from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import range
from usi.api import cci as api
from .callback import *
import sys

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

exists = api.exists

def read(name):
    if not exists(name):
        raise GSParamNonExistent
    return api.read(name)

def write(name, val):
    if isinstance(val, bool):
        val = int(val)
    if sys.version_info >= (3,0):
        api.write(str(name), str(val))
    else:
        api.write(unicode(name).encode('utf-8'), unicode(val).encode('utf-8'))

getType = api.get_type_string
getDocumentation = api.get_documentation
getProperties = api.get_properties

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
    is_array = False
    try:
        is_array = any(heads) and (sorted(set(range(len(heads)))) == sorted(set([int(x) for x in heads])))
    except ValueError:
        pass
    if is_array:
        # make a Python list if only sequential integer names at this level
        result = []
        for head in range(len(heads)):
            tails = breakdown[str(head)]
            if any(tails):
                # some further hierarchy
                result.append(makeDict(addIndex(name, head), tails, readProperties))
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
        for head, tails in breakdown.items():
            if any(tails):
                # some further hierarchy
                result[head] = makeDict(addIndex(name, head), tails, readProperties)
            else:
                # leaf
                index = addIndex(name, head)
                value = read(index)
                if api.is_bool(index):
                    value = value != '0' and value != 'false'
                elif api.is_float(index):
                    value = float(value)
                elif api.is_int(index):
                    value = int(value)

                if not api.is_array(index):
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
        all_params = api.list(addIndex(name,"*"))
        ln = len(name) + 1
    else:
        all_params = api.list("")
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
        for n, v in values.items():
            writeValueDict(addIndex(name, n), v)
        return
    if isinstance(values,list) or isinstance(values, tuple):
        # may be an embedded list?
        for i, v in enumerate(values):
            writeValueDict(addIndex(name, i), v)
        return
    # must be a leaf value
    write(name, values)

def printDict(params, indent=0):
    for name, value in params.items():
        if isinstance(value, dict):
            print((" " * indent) + name + ":")
            printDict(value, indent + 4)
            print("")
        elif isinstance(value, list):
            if any(value) and (isinstance(value[0], dict) or isinstance(value[0], list)):
                print((" " * indent) + name + ":")
                for index, val in enumerate(value):
                    print(" " * (indent + 4) + str(index) + ":")
                    printDict(val, indent + 8)
                    print('')
            else:
                print((" " * indent) + name + ": " + ', '.join(value))
        else:
            print((" " * indent) + name + ": " + str(value))

def filterDict(params, match, parents = [], result = {}):
    for name, value in params.items():
        if name == match:
            obj = result
            for parent in parents:
                obj = obj.setdefault(parent, {})
            obj[name] = value
        if isinstance(value, dict):
            result = filterDict(value, match, parents + [name], result)
    return result

def paramsToDict(params, base = ""):
    result = {}
    for name, value in params.items():
        if isinstance(value, dict):
            result.update(paramsToDict(value, addIndex(base, name)))
        elif isinstance(value, list):
            for index, val in enumerate(value):
              result.update(paramsToDict(val, addIndex(addIndex(base, name), index)))
        else:
            result[base] = value
    return result

