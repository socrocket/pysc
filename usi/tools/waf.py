def get_lockfile():
    import os
    import sys

    lockfilename = ".lock-waf_%s_build" % sys.platform
    directory = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

    while not lockfilename in os.listdir(directory) and directory != "":
        directory = os.path.dirname(directory)

    if directory == "":
        return None
    obj = {}
    with open(os.path.join(directory, lockfilename), "r") as script:
        code = compile(script.read(), os.path.join(directory, lockfilename), 'exec')
        exec(code, {}, obj)
    return obj

def get_lockfile_attr(key):
    obj = OBJECT
    if key:
        for idx in key.split('.') or []:
          obj = obj[idx]
    return obj

OBJECT = get_lockfile()
