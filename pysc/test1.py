import pysc
import json

@pysc.on("end_of_elaboration")
def do_elab(phase):
    print "Elab"
    print json.dumps(pysc.gc.readDict(), indent=2, sort_keys=True)
    #print pysc.gc.readDict()

@pysc.on("start_of_initialization")
@pysc.on("end_of_initialization")
@pysc.on("start_of_elaboration")
@pysc.on("end_of_simulation")
@pysc.on("start_of_evaluation")
@pysc.on("end_of_evaluation")
def do_phase(phase):
    print "Phase", phase

@pysc.on("start_of_simulation")
def do_start(phase):
    pysc.stop();

print "Start"

