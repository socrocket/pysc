
FACTORYSTORE = {}
OBJECTSTORE = {}

def usi_extend_delegate(obj):
    name = obj.name()
    print name
    if not name in OBJECTSTORE:
        OBJECTSTORE[name] = {}
    setattr(obj, 'if_extension', OBJECTSTORE[name])
