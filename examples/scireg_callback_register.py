import usi
import sys

@usi.on('start_of_simulation')
def simulation_begin(*k, **kw):
    gptimer = usi.USIDelegate('sdram')
    gptimer_conf = usi.USIDelegate('gptimer.register.conf')
    def foo(*k, **kw):
        print("Callback: Access at address {} with length of {} bytes on {}."\
                .format(k[0], k[1], k[2].scireg_get_string_attribute(scireg.SCIREG_NAME)))
    gptimer_conf.scireg_add_callback((foo, scireg.SCIREG_READ_ACCESS, long(0), long(4)))
    gptimer_conf.scireg_read(long(4)) # Kein Buszugriff, löst nicht aus
    gptimer.scireg_read(long(16)) # Buszugriff -> callback wird ausgelößt
    print('end of callback example')
    sys.exit()
