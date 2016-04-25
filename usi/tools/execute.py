import usi
import sys
import os.path

# Will be added in pysc/usi/tools/args.py
def argparse_init(parser):
    parser.add_argument('-s', '--script', dest='script', action='append', default=[], type=str, help='Execute script on start_of_initialization')

def execscript(name):
    with open(name, "r") as script:
        code = compile(script.read(), name, 'exec')
        exec(code, sys.modules['__main__'].__dict__)

def argparse_before_parse(args):
    for script in args.script:
        execscript(script)

@usi.on('start_of_initialization')
def start_of_initialization(*k, **kw):
    pass
