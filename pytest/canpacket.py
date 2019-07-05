import can
import bitstruct
import copy
import struct

from itertools import cycle
from collections import OrderedDict


class CanPacket(object):
    def __init__(self, **kwargs):
        self.message = None
        self.packet_info = OrderedDict()        
        self.totallength = 0
        self.pack_fmt = ''
        for k,v in kwargs.items():
            self.packet_info[k] = v
        
        for k,v in self.packet_info.items():
            self.totallength += int(v)
            self.pack_fmt += 'u'+ str(v)
        
    def parse(self, message):
        if type(message) is list:
            message = bytes(message)
        o = iter(bitstruct.unpack(self.pack_fmt,message))
        packet_data = OrderedDict()
        for k,v in self.packet_info.items():
            packet_data[k] = next(o)
        return packet_data

    def gen(self, *argv, **kwargs):
        pack_data = list()
        argv_it = iter(argv)

        for k,v in self.packet_info.items():
            if (len(argv) == 0):
                pack_data.append(kwargs[k])
            else:
                pack_data.append(next(argv_it))
                
        self.message = list(bitstruct.pack(self.pack_fmt, *pack_data))
        return self.message

    def update_crc(self):
        offsetbyte = -1        
        for k,v in self.packet_info.items():    # get crc offset from packet info
            if (k == 'crc'):
                offsetbyte = self._get_crc_offset()
                crc_length = int(v/8)
                break
        
        if offsetbyte == -1:    # if there are not crc, return without change
            return self.message

        for ii in range(crc_length):    # remove crc byte for calculating crc of message
            del self.message[offsetbyte]
        '''
        self.message
        CRC calculate logic
        '''
        crc = 0xab
        crc = crc.to_bytes(crc_length, byteorder='little', signed=False)
        for crc_byte in crc:    # put calculate crc value
            self.message.insert(offsetbyte,crc_byte)

        return self.message
        
    def _get_crc_offset(self):
        offsetbyte = 0
        for k,v in self.packet_info.items():
            if (k == 'crc'):
                break
            else:
                offsetbyte += v
        offsetbyte = int(offsetbyte / 8)
        return offsetbyte

if __name__ == "__main__":
    it = cycle([4,2,3,11,3,2,5])        
    ODS = CanPacket(reserv1=3,test=13,crc=8,reserv2=16,alive=8)
    _hex = lambda x : '%02X' % (x)
    for ii in range(0,20):
        msg = ODS.gen(reserv1=5,test=5,crc=0xa,reserv2=5,alive=next(it))
    #    print(' '.join(map(_hex,msg)))
        msg = ODS.update_crc()
        o = ODS.parse(msg)
        print(o)
        print(' '.join(map(_hex,msg)))