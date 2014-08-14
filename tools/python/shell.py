def help_text():
    print "SoCRocket - The Space TLM Framework"
def credits_text():
    print "Thomas Schuster, Rolf Meyer, Jan Wagner"
def copyright_text():
    print "(c) Copyright 2010-2014 TU-Braunschweig c3e"
def license_text():
    print "All rights reserved"

def start():
    import code
    try:
        import rlcompleter
        import readline
        import atexit
        import os

    except ImportError:
        print "Python shell enhancement modules not available."
    else:
        histfile = os.path.join(os.environ["HOME"], ".socrocket_history")
        rcfile = os.path.join(os.environ["HOME"], ".socrocketrc")
        #if 'libedit' in readline.__doc__:
        #    readline.parse_and_bind("bind ^I rl_complete")
        #else:
        readline.parse_and_bind("tab: complete")
        if os.path.isfile(histfile):
            readline.read_history_file(histfile)
        if os.path.isfile(rcfile):
            readline.read_init_file(rcfile)
        atexit.register(readline.write_history_file, histfile)
        del os, histfile, readline, rlcompleter, atexit
        print "Python shell history and tab completion are enabled."
    help = help_text
    credits = credits_text
    copyright = copyright_text
    license = license_text
    code.interact(local=locals(), banner='')

if __name__ == "__main__":
    start()