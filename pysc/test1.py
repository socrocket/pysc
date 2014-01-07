import pysc
import json

#@pysc.on("end_of_elaboration")
def do_elab(phase):
    print "Elab"
    print json.dumps(pysc.gc.readDict(), indent=2, sort_keys=True)
    #print pysc.gc.readDict()

def elf_file(name="", value="", time="", type=""):
    print "XX", name, value #, time, type

@pysc.on("end_of_initialization")
def do_init(phase):
    pysc.gc.on("ahbctrl.performance_counters.bytes_read", pysc.gc.post_write)(elf_file)

@pysc.on("start_of_initialization")
@pysc.on("start_of_elaboration")
@pysc.on("end_of_simulation")
@pysc.on("start_of_evaluation")
@pysc.on("end_of_evaluation")
def do_phase(phase):
    print "Phase", phase

#@pysc.on("start_of_simulation")
def do_start(phase):
    pysc.stop();

print "Start"

