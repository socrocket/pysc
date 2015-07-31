from __future__ import print_function
import pysc
import json

#@pysc.on("end_of_elaboration")
#def do_elab(phase):
#    print "Elab"
    #print json.dumps(pysc.gc.readValueDict(), indent=2, sort_keys=True)
    #print pysc.gc.readDict()

#def elf_file(name="", value="", time=None, type=None):
#    print "XX", name, value , time, type

#@pysc.on("end_of_initialization")
#def do_init(phase):
#    print "Init"
    #pysc.gc.on("ahbctrl.performance_counters.bytes_read", pysc.gc.post_write)(elf_file)

@pysc.on("start_of_initialization")
@pysc.on("end_of_initialization")
@pysc.on("start_of_elaboration")
@pysc.on("end_of_elaboration")
@pysc.on("start_of_simulation")
@pysc.on("end_of_simulation")
@pysc.on("start_of_evaluation")
@pysc.on("end_of_evaluation")
def do_phase(phase):
    print("Phase", phase)

@pysc.on("report")
def report(*args, **kwargs):
    print("XXXX report", args, kwargs)

#@pysc.on("start_of_simulation")
def do_start(phase):
    #import tools.python.shell as shell
    import pysc.api.gc as gc
    import gc as g
    g.collect()
    z = gc.readValueDict()
    a = gc.readPropertyDict()
    pysc.stop();
    g.collect()

print("Start")

@pysc.onCommand('APBUart')
def UARTInit(name):
    instance = pysc.api.amba.find(name)

    @pysc.onCommand(name)
    def uart_connect(port):
        import os
        if 'TMUX' in os.environ:
          import subprocess
          subprocess.Popen('tmux split-window -h "nc localhost %d"' % port)
