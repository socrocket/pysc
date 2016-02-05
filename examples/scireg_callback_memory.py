import usi
import sys

@usi.on('start_of_simulation')
def simulation_begin(*k, **kw):
    sdram = usi.USIDelegate('sdram')
    def foo(*k, **kw):
        print("Callback: Access at address {} with length of {} bytes on {}."\
                .format(k[0], k[1], k[2].scireg_get_string_attribute(scireg.SCIREG_NAME)))
    sdram.scireg_add_callback((foo, scireg.SCIREG_READ_ACCESS, long(0), long(4)))
    print('end of callback example')
    #sys.exit()
