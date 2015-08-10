
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
    for group in list(registry.get_group_names()):
        for klass in list(registry.get_module_names(group)):
            if registry.is_type(group, klass, obj) and not name in OBJECTSTORE:
                OBJECTSTORE[name] = {}
                OBJECTSTORE[name].update(usi_extend_creation(obj, klass))
            setattr(obj, 'if_data', OBJECTSTORE.setdefault(name, {}))
