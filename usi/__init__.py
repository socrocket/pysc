
__all__ = ["systemc", "api.delegate", "api.registry", "api.report"]

""" Standalone mode (embedded change this to False) """
__standalone__ = True


""" For context management """
__interpreter_name__ = ""

from usi.systemc import *
from usi.api.delegate import USIDelegate
from usi.api.registry import get_module_files
from usi.api import report

def find(name):
    """
      Finds SystemC sc_objects and returns USIDelegates to each matching object

      Simply provide the name: find('mctrl') -> [USIDelegate('mctrl')]
      Use dots to seperate in hierachy like in SystemC: find('top.leon3_0.mmu.tlb')
      The function can handle wildcards: find('mctrl') -> [USIDelegate('mctrl'), USIDelegate('mctrl.generics'), ...]
      To simplify the function always returns a list of USIDelegate objects.
    """
    result = []
    def recursive(objs):
        result = list(objs)
        for obj in list(objs):
            result += recursive(list(obj.children()))
        return result

    if name == "*":
        result += list(get_top_level_objects())
    elif name.endswith(".*"):
       obj = USIDelegate(name[:-2])
       result.append(obj)
    else:
       obj = USIDelegate(name)
       if not any(obj.get_if_tuple()):
         return []
       return [obj]

    result = recursive(result)
    return result

def refind(regex):
    import re
    if isinstance(regex, str):
        regex = re.compile(regex)

    allobj = find('*')
    results = []
    for obj in allobj:
        if regex.match(obj.name()):
            results.append(obj)
    return results

def add_to_reporting_list(name, severity, verbosity):
    if isinstance(name, list):
        for obj in name:
            add_to_reporting_list(obj, severity, verbosity)
    elif isinstance(name, str):
        add_to_reporting_list(find(name), severity, verbosity)
    elif isinstance(name, USIDelegate):
        report.add_sc_object_to_filter(name, severity, verbosity)
    else:
        raise Exception("Unknown Type")

def remove_from_reporting_list(name):
    if isinstance(name, list):
        for obj in name:
            remove_from_reporting_list(obj)
    elif isinstance(name, str):
        remove_from_reporting_list(find(name))
    elif isinstance(name, USIDelegate):
        report.remove_sc_object_from_filter(name)
    else:
        raise Exception("Unknown Type")

def get_current_callback():
    """May be a spawned thread or a call-in from C++, or in elaboration"""
    #ph = pysystemc.get_curr_process_handle()
    #if ph in PYCallback.active_callbacks.keys():
    #    st = PYCallback.active_callbacks[ph]
    #    if st:
    #        return st[-1]
    return None

def interpreter_name():
    """Return the interpreter name"""
    if __standalone__:
        return ""
    ccb = get_current_callback()
    if ccb:
        return ccb.interpreter_name

    else:
        return __interpreter_name__

# Exceptions and magic constants
class ThreadKill(Exception):
    pass

class ThreadReset(Exception):
    pass

class DuplicateThreadHandle(Exception):
    pass

class REPEAT_SPAWN:
    pass

class PromptStr:
    def __init__(self, iname, tname, tunit = NS):
        self.iname = iname
        self.tname = tname
        self.tunit = tunit
        self.tunitstr = TIME_UNITS[tunit]
    def __str__(self):
        return "(%s*%s @ %.6g %s) " % (
            self.iname, 
            self.tname, 
            simulation_time(self.tunit), 
            self.tunitstr
        )
    def strip(self):
        return "(%s::%s)" % (self.iname, self.tname)

class DebugWrapper:
    "Wrapper to run a thread inside the debugger"

    def __init__(self, runnable, prompt):
        import pdb
        self.debugger = pdb.Pdb()
        self.debugger.prompt = prompt
        self.runnable = runnable
        if hasattr(runnable, "func_name"):
          self.func_name = runnable.func_name

    def __call__(self, oargs, **nargs):
        return self.debugger.runcall(self.runnable, *oargs, **nargs)

# Callbacks and callback registration

# do not use the callback class because these are called from the SC
# elaboration process, not from an SC process.

# this binding can be changed by gs_winpdb
sc_callback_debug_wrapper = DebugWrapper

class SCCallback(object):
    def __init__(self, name):
        self.name = name
        self.all_runnables = dict()
    def register(self, runnable, obj=None, debug = False, time_unit = NS, keyargs = {}):
        if debug:
            runnable = sc_callback_debug_wrapper(runnable, PromptStr(interpreter_name(), self.name, time_unit))
        innm = interpreter_name()
        if innm not in self.all_runnables:
            self.all_runnables[innm] = []

        self.all_runnables[innm].append((runnable, keyargs))

    def call(self, *k, **kw):
        all_runners = self.all_runnables.get(interpreter_name(), [])
        for run, keyargs in all_runners:
            kw.update(**keyargs)
            try:
                run(*(k+(self.name,)), **kw)
            except Exception as e:
                import traceback, sys
                print "An exception occured in %s" % (self.name)
                print traceback.format_exc()
                sys.exit(1)

class SCCommand(object):
    def __init__(self):
        self.all_runnables = dict()
    def register(self, runnable, typename, debug = False, time_unit = NS, keyargs = {}):
        if debug:
            runnable = sc_callback_debug_wrapper(runnable, PromptStr(interpreter_name(), self.name, time_unit))
        if typename not in self.all_runnables:
            self.all_runnables[typename] = []

        self.all_runnables[typename].append((runnable, keyargs))
    
    def call(self, obj, typename, **kw):
        all_runners = self.all_runnables.get(typename, [])
        kw.update({"name":obj})
        for run, keyargs in all_runners:
            k = dict(kw)
            k.update(**keyargs)
            run(**k)

PHASE = {
    "start_of_initialization": SCCallback("start_of_initialization"),
    "end_of_initialization": SCCallback("end_of_initialization"),
    "start_of_elaboration": SCCallback("start_of_elaboration"),
    "end_of_elaboration": SCCallback("end_of_elaboration"),
    "start_of_simulation": SCCallback("start_of_simulation"),
    "end_of_simulation": SCCallback("end_of_simulation"),
    "start_of_evaluation": SCCallback("start_of_evaluation"),
    "end_of_evaluation": SCCallback("end_of_evaluation"),
    "pause_of_simulation": SCCallback("pause_of_simulation"),
    "report": SCCallback("report"),
    "command": SCCommand()
}

def on(phase, obj=None, debug=False, time_unit = NS, keyargs = {}):
    """Register phase sccallback handler"""
    def do(funct):
        if PHASE.has_key(phase):
            PHASE[phase].register(funct, obj, debug=debug, time_unit=time_unit, keyargs=keyargs)
        else:
            print "No such phase as %s" % (phase)
        return funct
    return do

def onCommandFrom(obj, debug=False, time_unit=NS, keyargs={}):
    return on("command", obj, debug, time_unit, keyargs)

from usi.tools import waf
import os
waf_out_dir = waf.get_lockfile_attr("out_dir")

for filename in get_module_files("module"):
    fullname = os.path.normpath(os.path.join(waf_out_dir, filename))
    pypath = os.path.splitext(fullname)[0] + ".py"
    pymodule = os.path.basename(os.path.splitext(fullname)[0])
    #print fullname, pypath, pyfile
    if os.path.exists(pypath):
        import imp
        imp.load_source(pymodule, pypath)
