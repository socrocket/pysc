import pysystemc

# Renaming time constants for easy reuse
FS = pysystemc.SC_FS
PS = pysystemc.SC_PS
NS = pysystemc.SC_NS
US = pysystemc.SC_US
MS = pysystemc.SC_MS
SEC = pysystemc.SC_SEC

"""Time constants units"""
TIME_UNITS = {
    FS:"fs", 
    PS:"ps", 
    NS:"ns", 
    US:"us", 
    MS:"ms", 
    SEC:"s"
}
'''
# Event
class FailedEventNotify(Exception):
    """An exception raised whenever an event nortification fails"""
    pass

class Event:
    "The event class"

    def __init__(self, obj=None):
        if obj == None:
            pysystemc.event_bind(self)
        else:
            pysystemc.event_bind(self, obj)

    def __del__(self):
      if pysystemc.event_remove:  pysystemc.event_remove(self)

    def notify(self, time=None, tu=None):
        if time == None:
            ng = pysystemc.event_notify(self)
        elif tu == None:
            ng = pysystemc.event_notify(self, time)
        else:
            ng = pysystemc.event_notify(self, time, tu)
        if not ng:  raise FailedEventNotify

    def wait(self):
        from pysc import thread_control
        pysystemc.wait(self)
        thread_control()

# Event Tree
class EventTree:
    """
        public interface:
          wait()
        creation:
            {Event | EventTree} {"&" | "|"} {Event | EventTree}
            objects of this class never exist.  
            It is a base class for two derived
            classes, in which the operator 
            (& or |) is implicit.
    """
    def __init__(self, left, right):
        """ both left and right must have a method "wait" """
        self.left = left
        self.right = right

    def __and__(self, tree):
        """
            operator overloading for creation of EventTree objects.
            these are the only officially 'public' constructors.
            the arguments must both be objects with a wait() method
        """
        return EventTreeAnd(self, tree)
    def __or__(self, tree): 
        """
            operator overloading for creation of EventTree objects.
            these are the only officially 'public' constructors.
            the arguments must both be objects with a wait() method
        """
        return EventTreeOr(self, tree)

    """
        add the operator overloads to the Event class as well so that
        combinations of Event become EventTree
    """
    Event.__and__ = __and__
    Event.__or__ = __or__

class EventTreeAnd(EventTree):
    """ class for an event tree whose topmost operator is an AND """
    def wait(self):
        """
            public interface consists of "wait", which waits 
            for both left.wait() and right.wait()
        """
        from pysc import thread_control, Fork
        Fork([self.left.wait, self.right.wait], wait_for=2)
        thread_control()

class EventTreeOr(EventTree):
    """ class for an event tree whose topmost operator is an OR """
    def wait(self):
        """
            public interface consists of "wait", which waits 
            for the earlier of left.wait() and right.wait()
        """
        from pysc import thread_control, Fork
        Fork([self.left.wait, self.right.wait], wait_for=1)
        thread_control()
'''
start = pysystemc.start
stop = pysystemc.stop
pause = pysystemc.pause
simulation_time = pysystemc.simulation_time
delta_count = pysystemc.delta_count
set_verbosity = pysystemc.set_verbosity
#spawn = pysystemc.spawn
is_running = pysystemc.is_running

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
        pysystemc.wait(obj)
    else:
        pysystemc.wait(obj, tu)
    # support for thread manipulation: pause, reset, kill, etc
    #thread_control()

# Utilities
def time(tu=None):
    if tu==None: tu=NS
    return "time=%d (delta=%d)" % (simulation_time(tu), delta_count())

