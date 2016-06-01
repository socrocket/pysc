import abc
from usi.api import sc_module as api
from usi import registry

NEW_STACK = []
def module_new(cls, *args, **kw):
    """First argument must be the sc_module instance name"""
    global NEW_STACK
    if len(NEW_STACK) and NEW_STACK[-1] == args[0]:
        result = object.__new__(cls)
        return result
    else:
        NEW_STACK.append(args[0])
        result = api.create_sc_module(cls, args, kw)
        NEW_STACK.pop()
        return result

class USIModuleMeta(abc.ABCMeta):
    def __init__(cls, name, bases, nmspc):
        super(USIModuleMeta, cls).__init__(name, bases, nmspc)
        cls.__new__ = staticmethod(module_new)
        registry.add_class_to_submodule("module", name, cls)

class USIModule(object):
    __metaclass__ = USIModuleMeta
    def start_of_elaboration(self):
        return
    def end_of_elaboration(self):
        return
    def start_of_simulation(self):
        return
    def end_of_simulation(self):
        return
