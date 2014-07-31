
__all__ = ["api.systemc"]

""" Standalone mode (embedded change this to False) """
__standalone__ = True


""" For context management """
__interpreter_name__ = ""

from pysc.api.systemc import *
from pysc.api import gc

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
'''
class PYCallback:
    "Manage any call from SystemC into Python that may enter user Python code"

    # tracking for callbacks and spawned threads
    active_callbacks = {}

    # Unique numbers - used only for debugging
    # do not use low numbers as this confuses Winpdb debugger
    next_callback_nr = 1000
    def callback_nr(self):
        PYCallback.next_callback_nr += 1
        return PYCallback.next_callback_nr

    def __init__(self, runnable, name=None, debug=False, time_unit=NS, \
          name_base="Callback", interpreter_name=None, \
          completed_event=None, args=(), keyargs={}):
        # Error check
        if not callable(runnable):
            raise TypeError, "Callback is non-callable: %s" % runnable

        # unique number
        self.nr = self.callback_nr()
        # callback name
        if name is None:
            if hasattr(runnable, "func_name"):
                self.name = runnable.func_name
            else:
                self.name = "Anon%s-%d" % (name_base, self.nr)
        else:
            self.name = name
        # name of interpreter
        if interpreter_name is None:
            self.interpreter_name = globals()["interpreter_name"]()
        else:
            self.interpreter_name = interpreter_name
        # Treat debug
        if debug:
            self.runnable = DebugWrapper(runnable, \
                PromptStr(self.interpreter_name, self.name, time_unit))
        else:
            self.runnable = runnable
        # args for callback function
        self.args = args
        self.keyargs = keyargs
        # callback status information
        self.kill_raised = False
        self.reset_raised = False
        self.pause_raised = False
        self.return_value = None
        self.started = False
        self.complete = False
        self.success = False
        self.resume_event = Event()
        self.completed_event = completed_event

        # now do something derived-class-specific
        self.end_of_init()

    def is_spawn(self):
        return False

    def end_of_init(self):
      """for a normal callback, just wait to be called"""
      pass

    def kill(self):
        self.kill_raised = True

    def reset(self):
        self.reset_raised = True

    def pause(self):
        if self.pause_raised == False:
            self.pause_raised = True

    def resume(self):
        if self.pause_raised == True:
            self.pause_raised = False
            self.resume_event.notify()

    def __call__(self):
        # manage the stack, then call the callback through run()
        sc_process = gsp_sc_get_curr_process_handle()
        if sc_process not in PYCallback.active_callbacks.keys():
            PYCallback.active_callbacks[sc_process] = []
        else:
            if self.is_spawn():
                raise DuplicateThreadHandle
        PYCallback.active_callbacks[sc_process].append(self)
        self.started = True
        try:
            self.run()
            self.success = True
        finally:
            # executed always, then any exception re-raised
            self.complete = True
            if self.completed_event:
                self.completed_event.notify()
            PYCallback.active_callbacks[sc_process].pop()
            if len(PYCallback.active_callbacks[sc_process]) == 0:
                del PYCallback.active_callbacks[sc_process]

    def run(self):
        # actually call the runnable, with kill, pause, loop, etc..
        while True:
            try:
                # launch the thread - return REPEAT_SPAWN to repeat
                return_value = self.runnable(*self.args, **self.keyargs)
                if return_value != REPEAT_SPAWN:
                    self.return_value = return_value
                    break
            except ThreadKill:
                # kills the thread cleanly
                return_value = None
                break
            except ThreadReset:
                # starts the thread again by iterating the while loop
                self.reset_raised = False

class ImmediateCallback(PYCallback):
    def end_of_init(self):
        self()

class Spawn(PYCallback):
    "Thread processes are a special case of callbacks"
    def is_spawn(self):
        return True
    def end_of_init(self):
        pysystemc.spawn(self, self.name)

def thread_control():
    this = get_current_callback()
    if this:
      if this.kill_raised:   
          # kill has higher priority over reset
          raise ThreadKill
      if this.reset_raised:  
          # reset has higher priority over pause
          raise ThreadReset
      if this.pause_raised:
          wait(this.resume_event)

class Fork:
    def __init__(self, runnable_list, wait_for=-1, kill=False, name="fork", args=None, keyargs=None, **spawnargs):

        assert pysystemc.get_curr_process_handle() != 0, "fatal error: pysc.fork should be used only inside processes"

        if not args:
            args = [() for x in runnable_list]
        if not keyargs:
            keyargs = [{} for x in runnable_list]

        nr_runnables = len(runnable_list)
        if wait_for < 0 or wait_for > nr_runnables:
            wait_for = nr_runnables

        done_ev = Event()
        self.spawns = [
            Spawn(runnable_list[i], "%s[%d]" % (name,i),
              args=args[i], keyargs=keyargs[i], completed_event=done_ev,
              **spawnargs)
            for i in range(nr_runnables)]

        while len([True for s in self.spawns if s.complete]) < wait_for:
            wait(done_ev)

        if kill:
            for p in self.spawns:  p.kill()
'''
# Callbacks and callback registration

# do not use the callback class because these are called from the SC
# elaboration process, not from an SC process.

# this binding can be changed by gs_winpdb
sc_callback_debug_wrapper = DebugWrapper

class SCCallback:
    def __init__(self, name):
        self.name = name
        self.all_runnables = dict()
    def __call__(self, runnable = False, debug = False, time_unit = NS, args = (), keyargs = {}):
        if runnable:
            self.register(runnable, debug, time_unit, args, keyargs)
        else:
            self.call(*args, **keyargs)

    def register(self, runnable, debug = False, time_unit = NS, args = (), keyargs = {}):
        if debug:
            runnable = sc_callback_debug_wrapper(runnable, PromptStr(interpreter_name(), self.name, time_unit))
        innm = interpreter_name()
        if innm not in self.all_runnables:
            self.all_runnables[innm] = []
        self.all_runnables[innm].append((runnable, args, keyargs))
    

    def call(self, *k, **kw):
        all_runners = self.all_runnables.pop(interpreter_name(), [])
        for run, args, keyargs in all_runners:
            key = dict(keyargs)
            key.update(kw)
            key.update(phase=self.name)
            print run
            run(*args, **key)


PHASE = {
    "start_of_initialization": SCCallback("start_of_initialization"),
    "end_of_initialization": SCCallback("end_of_initialization"),
    "start_of_elaboration": SCCallback("start_of_elaboration"),
    "end_of_elaboration": SCCallback("end_of_elaboration"),
    "start_of_simulation": SCCallback("start_of_simulation"),
    "end_of_simulation": SCCallback("end_of_simulation"),
    "start_of_evaluation": SCCallback("start_of_evaluation"),
    "end_of_evaluation": SCCallback("end_of_evaluation"),
    "report": SCCallback("report")
}

def on(phase, debug=False, time_unit = NS, args = (), keyargs = {}):
    """Register phase sccallback handler"""
    def do(funct):
        if PHASE.has_key(phase):
            PHASE[phase](funct, debug, time_unit, args, keyargs)
        else:
            print "No such phase as %s" % (phase)
        return funct
    return do

