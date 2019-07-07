import can

from scenario import Scenario
from canpacket import CanPacket
from itertools import cycle

_debug = lambda x : ' '.join(map(lambda y : '%02X' % (y),x))

def SendMessage(identifier, message):
    print('0x%04X  %s' % (identifier, _debug(message)))
    return True
    
def _TestVirtualMessage(CanMessage):
    import time
    it = cycle([0,1,2,2,2,0,1])
    CanMessage.gen(0,0,0,0,0,0,0,0,0,0)
    while(True):
        m = CanMessage.update({'lamp' : next(it)})
        time.sleep(0.1)
        yield m
    
if __name__ == "__main__":
    a = Scenario()
    a.init('scenario/test1.cfg')
    a.set_send_function(SendMessage)
    test_sequence = a.get_test_list()
    
    virtual_tester = _TestVirtualMessage(a.rx)

    for it in test_sequence:
        receive_message = next(virtual_tester)

        print('lamp status :', a.rx.parse(receive_message)['lamp'])
        
        if (a.is_send_method(it[0]) is True):
            r = it[1]({'dummy2' : a.rx.parse(receive_message)['lamp'] + 3 })
        else:
            pass
            r = it[1](receive_message)