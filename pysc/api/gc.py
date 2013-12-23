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
    return "%s.%s" % (name, index)

exists = pygc.exists

def read(name):
    if not exists(name):
        raise GSParamNonExistent
    return pygc.read(name)

def write(name, val):
    if isinstance(val, bool):
        val = int(val)
    pygc.write(name, str(val))

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

def makeDict(name, list_of_names):
    heads = set([getHead(x) for x in list_of_names])
    breakdown = dict((x,[]) for x in heads)
    for n in list_of_names:
        breakdown[getHead(n)].append(getTail(n))
    try:
        is_array = (set(range(len(heads))) == set([float(x) for x in heads]))
    except ValueError:
        is_array = False
    if is_array:
        # make a Python list if only sequential integer names at this level
        result = []
        for head in range(len(heads)):
            tails = breakdown[str(head)]
            if tails[0]:
                # some further hierarchy
                result.append(makeDict(addIndex(name, head),tails))
            else:
                # leaf
                result.append(read(addIndex(name, head)))
    else:
        # mixed names so make a dictionary
        result = {}
        for head,tails in breakdown.iteritems():
            if tails[0]:
                # some further hierarchy
                result[head] = makeDict(addIndex(name, head),tails)
            else:
                # leaf
                result[head] = read(addIndex(name, head))
    return result

def readDict(name):
    all_params = pygc.list(addIndex(name,"*"))
    ln = len(name) + 1
    all_params_list = [all_params.read(i)[ln:] for i in range(all_params.length())]
    return makeDict(name, all_params_list)

def writeDict(name, values):
    if isinstance(values,dict):
        # is it a dictionary?
        for n,v in values.iteritems():
            writeDict(addIndex(name, n),v)
        return
    if isinstance(values,list) or isinstance(values, tuple):
        # may be an embedded list?
        for i,v in enumerate(values):
            writeDict(addIndex(name, i),v)
        return
    # must be a leaf value
    write(name, values)
