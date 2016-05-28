from __future__ import print_function
from __future__ import absolute_import
import code
import os
import sys
try:
  from usi.usage import *
except ImportError:
  help_text = help
  credits_text = ""
  copyright_text = ""
  license_text = ""
from .console import Console

CONSOLE = None

def start(*k, **kw):
    global CONSOLE
    try:
        import rlcompleter
        import readline

    except ImportError:
        rlcompleter = None
        readline = None

    histfile = os.path.join(os.environ["HOME"], ".socrocket_history")
    rcfile = os.path.join(os.environ["HOME"], ".socrocketrc")

    if not CONSOLE:

        if not readline:
            print("Python shell enhancement modules not available.")
        else:
            if 'libedit' in readline.__doc__:
                readline.parse_and_bind("bind ^I rl_complete")
            else:
                readline.parse_and_bind("tab: complete")

            if os.path.isfile(histfile):
                readline.read_history_file(histfile)

            if os.path.isfile(rcfile):
                readline.read_init_file(rcfile)

            print("Python shell history and tab completion are enabled.")

        sys.modules['__main__'].__dict__.update({
          "help": help_text,
          "credits": credits_text,
          "copyright": copyright_text,
          "license": license_text
        })
        CONSOLE = Console(sys.modules['__main__'].__dict__)
        sys.modules['__main__'].__dict__['CONSOLE'] = CONSOLE

    CONSOLE.interact('')

    if readline:
        readline.write_history_file(histfile)

def stop(*k, **kw):
    global CONSOLE
    sys.modules['__main__'].CONSOLE.stop()

def is_running(*k, **kw):
    try:
        return sys.modules['__main__'].CONSOLE.run
    except:
        return False

def args(*k, **kw):
    from usi.tools.args import get_args
    ARGS = get_args()
    if ARGS.console:
        start()

def install():
    import usi
    from usi.tools.args import parser

    parser.add_argument('-c', '--console', dest='console', action='store_true', default=False, help='Execute an interactive python console right after start of the sc_main')

    usi.on("start_of_initialization")(args)
    #usi.on("start_of_simulation")(start)
    #usi.set_default_pause_handler(start)
    print('alternative')
    usi.on("pause_of_simulation")(usi.execute_default_pause_handler)
    #start()

try:
    install()
except ImportError:
    if __name__ == "__main__":
        start()
