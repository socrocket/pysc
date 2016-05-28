from __future__ import print_function
import usi.api.systemc as api

# Renaming time constants for easy reuse
FS = api.SC_FS
PS = api.SC_PS
NS = api.SC_NS
US = api.SC_US
MS = api.SC_MS
SEC = api.SC_SEC

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
  if api.is_running():
      if hasattr(api, "start"):
          api.start(*k)
      else:
          print("sc_start is not implemented")
  from usi import shell
  if shell.is_running():
      shell.stop()

def stop(*k, **kw):
  if api.is_running():
      api.stop()
  from usi import shell
  if shell.is_running():
      shell.stop()

def pause(*k, **kw):
  from usi import shell
  if not shell.is_running():
      api.pause()

simulation_time = api.simulation_time
delta_count = api.delta_count
set_verbosity = api.set_verbosity
#spawn = api.spawn
is_running = api.is_running
get_top_level_objects = api.get_top_level_objects

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
        api.wait(obj)
    else:
        api.wait(obj, tu)
    # support for thread manipulation: pause, reset, kill, etc
    #thread_control()

# Utilities
def time(tu=None):
    if tu==None: tu=NS
    return "time=%d (delta=%d)" % (simulation_time(tu), delta_count())

