import usi
import sys
from sr_register import scireg

@usi.on('start_of_simulation')
def simulation_begin(*k, **kw):
    reg0 = usi.USIDelegate('leon3_0.leon3.PC')
    def foo(*k, **kw):
        print("Callback: Access at address {} with length of {} bytes on {}."\
                .format(k[0], k[1], k[2].scireg_get_string_attribute(scireg.SCIREG_NAME)))
    reg0.scireg_add_callback((foo, scireg.SCIREG_READ_ACCESS, long(0), long(4)))
    #print('PC value: {}'.format(reg0.scireg_read(long(4))))
    print('end of callback example')
    #sys.exit()
