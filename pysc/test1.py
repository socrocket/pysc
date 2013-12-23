import pysc

def do_end_elab():
    print "End of Elab"

def do_start_sim():
    print "Start of Sim"
    pysc.stop()

def do_end_sim():
    print "End of Sim"

pysc.end_of_elaboration(do_end_elab)
pysc.start_of_simulation(do_start_sim)
pysc.end_of_simulation(do_end_sim)

print "Start"

