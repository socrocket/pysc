import usi
import sys
from sr_register import scireg
from usi.shell import start

print "Python started"

@usi.on('start_of_simulation')
def start2(*k, **kw):
    print "Zwei"

@usi.on('start_of_simulation')
def simulation_begin(*k, **kw):
    print "StartOfSimulation"
    start()
    

