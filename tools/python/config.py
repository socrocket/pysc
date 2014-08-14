import pysc
import sys

def load(*k, **kw):
    """Load initial model configuration"""
    from tools.python.arguments import parser
    parser.add_argument('-o', '--option', dest='option', action='append', type=str, help='Give configuration option')
    parser.add_argument('-p', '--python', dest='python', action='append', type=file, help='Execute python scripts')
    parser.add_argument('-j', '--json', dest='json', action='append', type=str, help='Read JSON configuration')
    parser.add_argument('-l', '--list', dest='list', action='store_true', help='List options')
    

def view(*k, **kw):
    """View detailed model configuration"""
    params = pysc.api.gc.readPropertyDict()
    params = pysc.api.gc.filterDict(params, "conf")
    pysc.api.gc.printDict(params)
    sys.exit()

def install():
    load()
    pysc.on("end_of_initialization")(view)

if __name__ == "__main__":
    install()
