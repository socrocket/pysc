import systemc_

# Renaming time constants for easy reuse
FS = systemc_.SC_FS
PS = systemc_.SC_PS
NS = systemc_.SC_NS
US = systemc_.SC_US
MS = systemc_.SC_MS
SEC = systemc_.SC_SEC

"""Time constants units"""
TIME_UNITS = {
    FS:"fs", 
    PS:"ps", 
    NS:"ns", 
    US:"us", 
    MS:"ms", 
    SEC:"s"
}

def start(*k, **kw):
  if systemc_.is_running():
      systemc_.start()
  from usi import shell
  if shell.is_running():
      shell.stop()

def stop(*k, **kw):
  if systemc_.is_running():
      systemc_.stop()
  from usi import shell
  if shell.is_running():
      shell.stop()

def pause(*k, **kw):
  from usi import shell
  if not shell.is_running():
      systemc_.pause()

simulation_time = systemc_.simulation_time
delta_count = systemc_.delta_count
set_verbosity = systemc_.set_verbosity
#spawn = systemc_.spawn
is_running = systemc_.is_running

def wait(obj, tu=None):
    """
       if obj is event or event tree, 
       call obj.wait(); else it is a scalar
    """
    #from pysc import thread_control
    if hasattr(obj, "wait"):
        obj.wait()
        return
    if tu == None:
        systemc_.wait(obj)
    else:
        systemc_.wait(obj, tu)
    # support for thread manipulation: pause, reset, kill, etc
    #thread_control()

# Utilities
def time(tu=None):
    if tu==None: tu=NS
    return "time=%d (delta=%d)" % (simulation_time(tu), delta_count())

