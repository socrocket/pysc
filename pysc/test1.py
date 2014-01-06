import pysc

@pysc.on("end_of_elaboration")
@pysc.on("start_of_simulation")
@pysc.on("end_of_simulation")
def do_phase(phase):
    print "Phase", phase

print "Start"

