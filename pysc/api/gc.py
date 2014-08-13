import pygc

"""
1) GC Database Access
This allows GreenScript to act as a configuration tool or parser.

These functions use full hierarchical names.  The name of the Python
interpreter (the GreenScriptModule) is not prepended to the names supplied
by the user.
"""

class GSParamNonExistent(Exception):
    pass

def addIndex(name, index):
    if name != "" and index != "":
        return "%s.%s" % (name, index)
    elif name != "":
        return name
    else:
        return index

exists = pygc.exists

def read(name):
    if not exists(name):
        raise GSParamNonExistent
    return pygc.read(name)

def write(name, val):
    if isinstance(val, bool):
        val = int(val)
    pygc.write(name, str(val))

getType = pygc.get_type_string
getDocumentation = pygc.get_documentation
getProperties = pygc.get_properties

def readList(name):
    result = []
    index = 0
    while True:
        ni = addIndex(name, index)
        if not exists(ni):
            break
        result.append(read(ni))
        index += 1
    return result

def writeList(name, values):
    for i, v in enumerate(values):
        write(addIndex(name, i), v)

def getHead(name):
    return name.split(".")[0]

def getTail(name):
    return name[len(getHead(name))+1:]

def makeDict(name, list_of_names, readProperties = False):
    heads = set([getHead(x) for x in list_of_names])
    heads.discard('')
    breakdown = dict((x, []) for x in heads)
    try:
        list_of_names.remove('')
    except ValueError:
        pass
    for n in list_of_names:
        breakdown[getHead(n)].append(getTail(n))
    try:
        is_array = (sorted(set(range(len(heads)))) == sorted(set([int(x) for x in heads])))
    except ValueError:
        is_array = False
    if is_array:
        # make a Python list if only sequential integer names at this level
        result = []
        for head in range(len(heads)):
            tails = breakdown[str(head)]
            if any(tails):
                # some further hierarchy
                result.append(makeDict(addIndex(name, head), tails), readProperties)
            else:
                # leaf
                index = addIndex(name, head)
                if not readProperties:
                    result.append(read(index))
                else:
                    properties = dict(getProperties(index))
                    properties["documentation"] = getDocumentation(index)
                    properties["type"] = getType(index)
                    properties["value"] = read(addIndex(name, head))
                    result.append(properties)
    else:
        # mixed names so make a dictionary
        result = {}
        for head, tails in breakdown.iteritems():
            if any(tails):
                # some further hierarchy
                result[head] = makeDict(addIndex(name, head), tails, readProperties)
            else:
                # leaf
                index = addIndex(name, head)
                value = read(index)
                if pygc.is_bool(index):
                    value = bool(value)
                elif pygc.is_float(index):
                    value = float(value)
                elif pygc.is_int(index):
                    value = int(value)

                if not pygc.is_array(index):
                    if not readProperties:
                        result[head] = value
                    else:
                        properties = dict(getProperties(index))
                        properties["documentation"] = getDocumentation(index)
                        properties["type"] = getType(index)
                        properties["value"] = value
                        result[head] = properties
    return result

def listParams(name = ""):
    if name != "":
        all_params = pygc.list(addIndex(name,"*"))
        ln = len(name) + 1
    else:
        all_params = pygc.list("")
        ln = 0

    return [all_params.read(i)[ln:] for i in range(all_params.length())]

def readPropertyDict(name = ""):
    all_params_list = listParams(name)
    return makeDict(name, all_params_list, True)

def readValueDict(name = ""):
    all_params_list = listParams(name)
    return makeDict(name, all_params_list, False)

def writeValueDict(name, values):
    if isinstance(values, dict):
        # is it a dictionary?
        for n, v in values.iteritems():
            writeDict(addIndex(name, n), v)
        return
    if isinstance(values,list) or isinstance(values, tuple):
        # may be an embedded list?
        for i, v in enumerate(values):
            writeDict(addIndex(name, i), v)
        return
    # must be a leaf value
    write(name, values)

pre_read = pygc.pre_read
post_read = pygc.post_read
reject_write = pygc.reject_write
pre_write = pygc.pre_write
post_write = pygc.post_write
create_param = pygc.create_param
destroy_param = pygc.destroy_param
post_write_and_destroy = pygc.post_write_and_destroy
no_callback = pygc.no_callback

register = pygc.register_callback
unregister = pygc.unregister_callback

def on(name, type):
    def do(funct):
        return register(name, funct, type)
    return do
