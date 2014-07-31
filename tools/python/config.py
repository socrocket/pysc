import pysc
import sys

def print_params(params, indent=0):
    for name, value in params.iteritems():
        if isinstance(value, dict):
            print (" " * indent) + name + ":"
            print_params(value, indent + 4)
            print
        elif isinstance(value, list):
            if any(value) and (isinstance(value[0], dict) or isinstance(value[0], list)):
                print (" " * indent) + name + ":"
                for index, val in enumerate(value):
                    print " " * (indent + 4) + str(index) + ":"
                    print_params(val, indent + 8)
                    print
            else:
                print (" " * indent) + name + ": " + ', '.join(value)
        else:
            print (" " * indent) + name + ": " + str(value)
            
def param_filter(params, match, parents = []):
    result = {}
    for name, value in params.iteritems():
        if name == match:
            obj = result
            for parent in parents:
              obj[parent] = {}
              obj = obj[parent]
            obj[name] = value
        if isinstance(value, dict):
            result.update(param_filter(value, match, parents + [name]))
    return result

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
    print_params(params)
    params = param_filter(params, "conf")
    sys.exit()

def install():
    load()
    pysc.on("end_of_initialization")(view)

if __name__ == "__main__":
    install()
