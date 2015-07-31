
FACTORYSTORE = {}
OBJECTSTORE = {}

def attach(klass, name, member):
    FACTORYSTORE.setdefault(klass, {})[name] = member

def usi_extend_creation(obj, klass):
    result = {}
    for name, item in FACTORYSTORE.get(klass, {}).items():
        i = item
        if hasattr(item, '__call__'):
            i = item.__get__(obj)
        result[name] = i
    return result

def usi_extend_delegate(obj):
    """
       Must be documentet!
       Why this might be a bad idea for bound functions!
       (Garbage collector)
       Object cache?
      
    """
    from sr_registry import sr_registry as registry
    name = obj.name()
    klass = registry.get_type_of(obj)
    if not name in OBJECTSTORE:
        OBJECTSTORE[name] = usi_extend_creation(obj, klass)
    setattr(obj, 'if_data', OBJECTSTORE[name])
