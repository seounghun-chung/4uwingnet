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
_debug = lambda x : ' '.join(map(_hex,x)) if type(x) is list else x

class Error(Exception):
    pass
    
    
class Scenario(object):
    def __init__(self, *argv, **kwargs):
        self.alivecycle = cycle([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
        self.base_txpacket = dict()
        self.type_of_method = dict()
        
    def set_send_function(self,pf_send):
        ''' register send bus method '''
        self._send = pf_send

    def get_test_list(self):
        ''' 
        self.sequence[0] : pattern (o,c,a,f,q,d)
        self.sequence[1] : funtion pointer (dependant of pattern)
           {o,c,a,f} : _ready_to_data_for_sending
           {q,d} : _check_fault
        '''
        return self.sequence
        
    def is_send_method(self, step):
        '''
        check type of sequence method type
        '''
        if self.type_of_method[step] == 'receive':
            return False
        else:
            return True
        
        
    def init(self,path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(path)

        self.base_txpacket = self.cfg._sections['tx_default']
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
                    l = self._make_ok_function(self.base_txpacket)
                    self.type_of_method[step] = 'send'
                    self.sequence.append((step,l))

            elif step == 'c': # make crc packet  (alive update, no crc update)
                for _ in range(size):
                    l = self._make_crc_function(self.base_txpacket)
                    self.type_of_method[step] = 'send'                    
                    self.sequence.append((step,l))
                 
            elif step == 'a': # make alive packet  (alive update twice, crc update)
                for _ in range(size):
                    l = self._make_alive_function(self.base_txpacket)
                    self.type_of_method[step] = 'send'                    
                    self.sequence.append((step,l))
                
            elif step == 'f': # make alive packet  (alive update and set 0xf, crc update)
                for _ in range(size):
                    l = self._make_alive_f_function(self.base_txpacket)
                    self.type_of_method[step] = 'send'                    
                    self.sequence.append((step,l))
   
            elif step == 'q':
                l = lambda x: self._check_fault(x, self.cfg.getint('TestConfig','rx_sig_qual'))
                self.sequence.append((step,l))
                self.type_of_method[step] = 'receive'   
            elif step == 'd':
                l = lambda x: self._check_fault(x, self.cfg.getint('TestConfig','rx_sig_dequal'))
                self.sequence.append((step,l))
                self.type_of_method[step] = 'receive'  
            else:
                raise RuntimeError('%c is not defined in sequence' % step)
            
    def _make_ok_function(self, default_packet):
        def __packet(packet = None):
            ready_packet = copy.deepcopy(default_packet)
            if packet is not None:
                ready_packet.update(packet)
            ready_packet['alive'] = next(self.alivecycle)
            msg = self.tx.gen(**ready_packet)
            msg = self.tx.update_crc()
            return msg

        l = partial(self._ready_to_data_for_sending, int(self.cfg.get('TestConfig','txid'),16), __packet)                   
        return l
    
    def _make_crc_function(self,default_packet):
        def __packet(packet = None):
            ready_packet = copy.deepcopy(default_packet)
            if packet is not None:
                ready_packet.update(packet)
            ready_packet['alive'] = next(self.alivecycle)
            ready_packet['crc'] = 0xff
            msg = self.tx.gen(**ready_packet)
            return msg
        
        l = partial(self._ready_to_data_for_sending, int(self.cfg.get('TestConfig','txid'),16), __packet)                   
        return l
        
    def _make_alive_function(self,default_packet):
        def __packet(packet = None):
            ready_packet = copy.deepcopy(default_packet)
            if packet is not None:
                ready_packet.update(packet)
            ''' count up twice for breaking alive '''
            ready_packet['alive'] = next(self.alivecycle)
            ready_packet['alive'] = next(self.alivecycle)
            msg = self.tx.gen(**ready_packet)
            msg = self.tx.update_crc()       
            return msg
            
        l = partial(self._ready_to_data_for_sending, int(self.cfg.get('TestConfig','txid'),16), __packet)                   
        return l
        
    def _make_alive_f_function(self,default_packet):
        def __packet(packet = None):
            ready_packet = copy.deepcopy(default_packet)
            if packet is not None:
                ready_packet.update(packet)
            ready_packet['alive'] = next(self.alivecycle)
            ready_packet['alive'] = 0xf
            msg = self.tx.gen(**ready_packet)
            msg = self.tx.update_crc()        
            return msg
        
        l = partial(self._ready_to_data_for_sending, int(self.cfg.get('TestConfig','txid'),16), __packet)                   
        return l
        
    def _check_fault(self, recv_message, expected):
        ''' check to receive expected value '''
        parsed_recv_message = self.rx.parse(recv_message)
        print('test',parsed_recv_message[self.cfg.get('TestConfig','rx_sig_check')], expected)
        if (parsed_recv_message[self.cfg.get('TestConfig','rx_sig_check')] == expected):
            return True
        else:
            return False
        
    def _ready_to_data_for_sending(self, canid, pf_gen, base_message=None):
        ''' lambda function for sending data. it is stored in list sequence'''        
        if (type(base_message) is bytes):
            base_message = self.tx.parse(base_message)
        elif (type(base_message) is list):
            base_message = self.tx.parse(bytes(base_message))
        elif (type(base_message) is str):
            base_message = self.tx.parse(bytes.fromhex(base_message))

        msg = pf_gen(base_message)        
        return self._send(canid, msg)
        
    def _send(self, identifier, message):
        ''' 
        virtual function for sending CAN data 
        shall register CAN send method 
            
        identifier : int
        message    : list 
        '''
        print('ERR : set_send_function', identifier, _debug(message))
        return False  

        
    def dbg(self):  
        index = 0
        it = iter(self.sequence)

        next(it)[1]({'dummy3' : 0xbb})
        next(it)[1]('123456abcdef7856')
        
        for seq in it:
            r = seq[1]({'dummy3' : 0xaa})
            index += 1
            
if __name__ == "__main__":
    a = Scenario()
    a.init('scenario/test1.cfg')
    a.dbg()