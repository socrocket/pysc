import pysc
import sys
import json
from tools.python.arguments import parser, args

"""Load initial model configuration"""
parser.add_argument('-o', '--option', dest='option', action='append', default=[], type=str, help='Give configuration option')
parser.add_argument('-j', '--json', dest='json', action='append', default=[], type=str, help='Read JSON configuration')
parser.add_argument('-l', '--list', dest='list', action='store_true', help='List options')
    
@pysc.on("start_of_initialization")
def parse_args(*k, **kw):
    for jsonfile in args().json:
        with open(jsonfile) as openfile:
            json.load(openfile)
    for option in args().option:
        l = option.split('=')
        if len(l) == 2:
            name = l[0]
            value = l[1]
            if pysc.api.gc.exists(name):
                pysc.api.gc.write(name, value)
            else:
                print "Option does not exist"
                sys.exit(1)
        else:
            print "Option malformated '%s', it needs to be formated 'key=value'" % option
            sys.exit(1)

@pysc.on("end_of_initialization")
def show_configuration(*k, **kw):
    """View detailed model configuration"""
    if args().list:
        params = pysc.api.gc.readPropertyDict()
        pysc.api.gc.printDict(params)
        params = pysc.api.gc.filterDict(params, "generics")
        sys.exit()
