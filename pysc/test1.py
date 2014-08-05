import pysc
import json

@pysc.on("end_of_elaboration")
def do_elab(phase):
    print "Elab"
    #print json.dumps(pysc.gc.readValueDict(), indent=2, sort_keys=True)
    #print pysc.gc.readDict()

def elf_file(name="", value="", time="", type=""):
    print "XX", name, value #, time, type

@pysc.on("end_of_initialization")
def do_init(phase):
    print "Init"
    #pysc.gc.on("ahbctrl.performance_counters.bytes_read", pysc.gc.post_write)(elf_file)

@pysc.on("start_of_initialization")
@pysc.on("start_of_elaboration")
@pysc.on("end_of_simulation")
@pysc.on("start_of_evaluation")
@pysc.on("end_of_evaluation")
def do_phase(phase):
    print "Phase", phase

@pysc.on("report")
def report(phase, report):
    print "XXXX report"
    pass

@pysc.on("start_of_simulation")
def do_start(phase):
    #import tools.python.shell as shell
    import pysc.api.gc as gc
    import gc as g
    g.collect()
    print "Test 1"
    x = gc.readValueDict()
    print "Test 2"
    y = gc.readPropertyDict()
    print "Test 3"
    x = gc.readValueDict()
    print "Test 4"
    b = gc.readPropertyDict()
    print "Test 5"
    x = gc.readValueDict()
    print "Test 6"
    c = gc.readPropertyDict()
    print "Test 7"
    x = gc.readValueDict()
    print "Test 8"
    d = gc.readPropertyDict()
    print "Test 9"
    x = gc.readValueDict()
    print "Test 10"
    e = gc.readPropertyDict()
    print "Test 11"
    x = gc.readValueDict()
    print "Test 12"
    f = gc.readPropertyDict()
    print "Test 13"
    x = gc.readValueDict()
    print "Test 14"
    g_ = gc.readPropertyDict()
    print "Test 15"
    x = gc.readValueDict()
    print "Test 16"
    h = gc.readPropertyDict()
    print "Test 17"
    z = gc.readValueDict()
    print "Test 18"
    a = gc.readPropertyDict()
    print "Test 19"
    del a, b, c, d, e
    print "Test 20"
    #shell.start()
    pysc.stop();
    g.collect()

print "Start"

