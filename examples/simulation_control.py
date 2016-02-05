from __future__ import print_function
import usi
from usi import shell

def onpause(*k, **kw):
    print('current simulation time: {} ns'.format(usi.systemc.simulation_time(usi.NS)))
    #usi.start()
    #usi.start(1000.0, usi.NS)
    shell.start()

usi.set_default_pause_handler(onpause)
