import can
import bitstruct
import copy
import struct
import configparser

from canpacket import CanPacket
from itertools import cycle
from functools import partial
from collections import OrderedDict

_hex = lambda x : '%02X' % (x)
_debug = lambda x : ' '.join(map(_hex,x))

class Scenario(object):
    def __init__(self, *argv, **kwargs):
        pass

    def init(self,path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(path)
        
        for k,v in self.cfg._sections['rx'].items():
            self.cfg._sections['rx'][k] = int(v)
        for k,v in self.cfg._sections['tx'].items():
            self.cfg._sections['tx'][k] = int(v)

        self.sequence = list()
        self.rx = CanPacket(**self.cfg._sections['rx'])
        self.tx = CanPacket(**self.cfg._sections['tx'])

        sequence_str = self.cfg.get('pattern','sequence').replace(' ','')
        alivecycle = cycle([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])

        for step in sequence_str:                    
            if step == 'o': # make normal packet  (alive update, crc update)
                for k, v in self.cfg._sections['tx_default'].items():
                    self.cfg._sections['tx_default'][k] = int(v)
                    if (k == 'alive'):
                        self.cfg._sections['tx_default'][k] = next(alivecycle)            
                msg = self.tx.gen(**self.cfg._sections['tx_default'])
                msg = self.tx.update_crc()
                l = partial(self._send, int(self.cfg.get('TestConfig','txid'),16), msg)                   
                self.sequence.append(l)

            elif step == 'c': # make crc packet  (alive update, no crc update)
                for k, v in self.cfg._sections['tx_default'].items():
                    self.cfg._sections['tx_default'][k] = int(v)
                    if (k == 'alive'):
                        self.cfg._sections['tx_default'][k] = next(alivecycle)            
                msg = self.tx.gen(**self.cfg._sections['tx_default'])
                l = partial(self._send, int(self.cfg.get('TestConfig','txid'),16), msg)                      
                self.sequence.append(l)
                 
            elif step == 'a': # make alive packet  (alive update twice, crc update)
                for k, v in self.cfg._sections['tx_default'].items():
                    self.cfg._sections['tx_default'][k] = int(v)
                    if (k == 'alive'):
                        self.cfg._sections['tx_default'][k] = next(alivecycle)            
                        self.cfg._sections['tx_default'][k] = next(alivecycle)            
                        
                msg = self.tx.gen(**self.cfg._sections['tx_default'])
                msg = self.tx.update_crc()
                l = partial(self._send, int(self.cfg.get('TestConfig','txid'),16), msg)
                self.sequence.append(l)
                
            elif step == 'f': # make alive packet  (alive update and set 0xf, crc update)
                for k, v in self.cfg._sections['tx_default'].items():
                    self.cfg._sections['tx_default'][k] = int(v)
                    if (k == 'alive'):
                        self.cfg._sections['tx_default'][k] = next(alivecycle)     
                        self.cfg._sections['tx_default'][k] = 0xf                
                        
                msg = self.tx.gen(**self.cfg._sections['tx_default'])
                msg = self.tx.update_crc()
                l = partial(self._send, int(self.cfg.get('TestConfig','txid'),16), msg)       
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
        print(canid, _debug(message), dummy)
        return True
        
    def dbg(self):  
        for seq in self.sequence:
            r = seq(bytes.fromhex('2234abcd1234abcd'))
            print(r)
            
if __name__ == "__main__":
    a = Scenario()
    
    def send(canid, msg, dummy):
        print('hello',msg,dummy)
    a._send = send
    a.init('scenario/test1.cfg')
    a.dbg()