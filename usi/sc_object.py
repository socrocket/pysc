
FACTORYSTORE = {}
OBJECTSTORE = {}

def usi_extend_delegate(obj):
    """
       Must be documentet!
       Why this might be a bad idea for bound functions!
       (Garbage collector)
       Object cache?
      
    """
    name = obj.name()
    if not name in OBJECTSTORE:
        OBJECTSTORE[name] = {}
    setattr(obj, 'if_data', OBJECTSTORE[name])
