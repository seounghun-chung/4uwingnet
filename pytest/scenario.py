import can
import bitstruct
import copy
import struct
import configparser
import re

from canpacket import CanPacket
from itertools import cycle
from functools import partial
from collections import OrderedDict

_hex = lambda x : '%02X' % (x)
_debug = lambda x : ' '.join(map(_hex,x)) if type(x) is str else x

class Error(Exception):
    pass
    
    
class Scenario(object):
    def __init__(self, *argv, **kwargs):
        self.alivecycle = cycle([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
        self.base_txpacket = dict()

    def set_send_function(self,pf_send):
        ''' register send message virtual function '''
        self._send = pf_send
        
    def init(self,path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(path)

        self.base_txpacket = copy.deepcopy(self.cfg._sections['tx_default'])
        for k,v in self.cfg._sections['rx'].items():
            self.cfg._sections['rx'][k] = int(v)
        for k,v in self.cfg._sections['tx'].items():
            self.cfg._sections['tx'][k] = int(v)

        self.sequence = list()
        self.rx = CanPacket(**self.cfg._sections['rx'])
        self.tx = CanPacket(**self.cfg._sections['tx'])

        ''' test sequence parsing '''
        sequence_str = self.cfg.get('pattern','sequence').replace(' ','')
        parsed_infos = re.findall(r'([<>]?)([a-zA-Z])(\d+)(\s*)', sequence_str)    
        if ''.join([''.join(info) for info in parsed_infos]) != sequence_str:
            raise Error("bad format '{}'".format(sequence_str))
                    
        for parsed_info in parsed_infos:   
            step = parsed_info[1]
            size = int(parsed_info[2])
            
            if size == 0:
                raise Error("bad format '{}'".format(fmt + byte_order))
            
            if   step == 'o': # make normal packet  (alive update, crc update)
                for _ in range(size):
                    l,msg = self._make_ok_function(self.base_txpacket)
                    self.sequence.append(l)

            elif step == 'c': # make crc packet  (alive update, no crc update)
                for _ in range(size):
                    l,msg = self._make_crc_function(self.base_txpacket)
                    self.sequence.append(l)
                 
            elif step == 'a': # make alive packet  (alive update twice, crc update)
                for _ in range(size):
                    l,msg = self._make_alive_function(self.base_txpacket)
                    self.sequence.append(l)
                
            elif step == 'f': # make alive packet  (alive update and set 0xf, crc update)
                for _ in range(size):
                    l,msg = self._make_alive_f_function(self.base_txpacket)
                    self.sequence.append(l)
   
            elif step == 'q':
                l = lambda x: self._check_fault(x, self.cfg.getint('TestConfig','rx_sig_qual'))
                self.sequence.append(l)

            elif step == 'd':
                l = lambda x: self._check_fault(x, self.cfg.getint('TestConfig','rx_sig_dequal'))
                self.sequence.append(l)

            else:
                raise RuntimeError('%c is not defined in sequence' % step)
                
            print(step, _debug(msg))               

            
    def _make_ok_function(self, packet):
        packet['alive'] = next(self.alivecycle)
        msg = self.tx.gen(**packet)
        msg = self.tx.update_crc()

        def __packet(packet):
            packet['alive'] = next(self.alivecycle)
            msg = self.tx.gen(**packet)
            msg = self.tx.update_crc()
                
        l = partial(self._send, int(self.cfg.get('TestConfig','txid'),16), __packet)                   
        return (l,msg)
    
    def _make_crc_function(self,packet):
        packet['alive'] = next(self.alivecycle)
        msg = self.tx.gen(**packet)
        
        l = partial(self._send, int(self.cfg.get('TestConfig','txid'),16), msg)                      
        return (l,msg)
        
    def _make_alive_function(self,packet):
        packet['alive'] = next(self.alivecycle)
        packet['alive'] = next(self.alivecycle)
        msg = self.tx.gen(**packet)
        msg = self.tx.update_crc()       
        
        l = partial(self._send, int(self.cfg.get('TestConfig','txid'),16), msg)                      
        return (l,msg)
        
    def _make_alive_f_function(self,packet):
        packet['alive'] = next(self.alivecycle)
        packet['alive'] = 0xf
        msg = self.tx.gen(**packet)
        msg = self.tx.update_crc()        
        
        l = partial(self._send, int(self.cfg.get('TestConfig','txid'),16), msg)                      
        return (l,msg)
        
    def _check_fault(self, recvmsg, expected):
        ''' check to receive expected value '''
        d = self.rx.parse(recvmsg)
        print('test',d[self.cfg.get('TestConfig','rx_sig_check')], expected)
        if (d[self.cfg.get('TestConfig','rx_sig_check')] == expected):
            return True
        else:
            return False
        
    def _send(self, canid, message, dummy):
        ''' virtual function , shall be defined before executing init function. (because of partial function)
            dummy is compatible with recv feature...... it is not used'''
        print('ERR : set_send_function', canid, _debug(message), dummy)
        return True
        
    def update_base_txpacket(self, signame, value):
        self.base_txpacket[signame] = value    
        
    def dbg(self):  
        index = 0
        it = iter(self.sequence)

        for seq in it:
            r = seq(bytes.fromhex('2234abcd1234ab%02d' % index))
            index += 1
            
if __name__ == "__main__":
    a = Scenario()
    
    def send(canid, msg, dummy):
        print('hello',msg,dummy)
#    a._send = send
    a.init('scenario/test1.cfg')
    a.dbg()