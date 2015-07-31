import usi
import sys
from usi.tools.args import parser, get_args

parser.add_argument('-s', '--script', dest='script', action='append', default=[], type=str, help='Execute script on start_of_initialization')

def execscript(name):
    with open(name, "r") as script:
        code = compile(script.read(), name, 'exec')
        exec(code, sys.modules['__main__'].__dict__)

@usi.on('start_of_initialization')
def start_of_initialization(*k, **kw):
    for script in get_args().script:
        execscript(script)
