import can
import time

from scenario import Scenario
from canpacket import CanPacket
from itertools import cycle
from datetime import datetime

_debug = lambda x : ' '.join(map(lambda y : '%02X' % (y),x))
global_timer_start = 0
global_timer_end = 0

def SendMessage(identifier, message):
    print(datetime.now(), '0x%04X  %s' % (identifier, _debug(message)))
    return True
    
    
def _TestVirtualMessage(CanMessage):
    it = cycle([0,1,2,2,2,0,1])
    CanMessage.gen(0,0,0,0,0,0,0,0,0,0)
    while(True):
        time.sleep((1 - (global_timer_end - global_timer_start)))
        m = CanMessage.update({'lamp' : next(it)})
        yield m

        
if __name__ == "__main__":
    a = Scenario()
    a.init('scenario/test1.cfg')
    a.set_send_function(SendMessage)
    test_sequence = a.get_test_list()
    
    virtual_tester = _TestVirtualMessage(a.rx)

    for it in test_sequence:        
        # wait for receiving message

        receive_message = next(virtual_tester)

        global_timer_start = time.time() # virtual timer test
        
        print(datetime.now(), 'lamp status :', a.rx.parse(receive_message)['lamp'])
        
        if (a.is_send_method(it[0]) is True):
            r = it[1]({'dummy2' : a.rx.parse(receive_message)['lamp'] + 3 })
        else:
            pass
            r = it[1](receive_message)
            
        global_timer_end = time.time() # virtual timer test