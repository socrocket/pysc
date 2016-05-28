
FACTORYSTORE = {}
OBJECTSTORE = {}

def attach(klass, name, member):
    FACTORYSTORE.setdefault(klass, {})[name] = member

def usi_extend_creation(group, klass, obj):
    result = {}
    for name, item in FACTORYSTORE.get("{}.{}".format(group, klass), {}).items():
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
    from sr_registry import api
    if obj and obj.this and hasattr(obj, 'name') and callable(obj.name):
        name = obj.name()
        if not name in OBJECTSTORE:
            for group in list(api.get_group_names()):
                for klass in list(api.get_module_names(group)):
                    if api.is_type(group, klass, obj):
                        OBJECTSTORE[name] = {}
                        OBJECTSTORE[name].update(usi_extend_creation(group, klass, obj))
        setattr(obj, 'if_data', OBJECTSTORE.setdefault(name, {}))
