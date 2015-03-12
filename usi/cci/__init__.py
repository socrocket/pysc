import usi
import sys
import json
import usi.api.parameter
from usi.tools.args import parser, get_args

"""Load initial model configuration"""
parser.add_argument('-o', '--option', dest='option', action='append', default=[], type=str, help='Give configuration option')
parser.add_argument('-j', '--json', dest='json', action='append', default=[], type=str, help='Read JSON configuration')
parser.add_argument('-l', '--list', dest='list', action='store_true', help='List options')
    
@usi.on("start_of_initialization")
def parse_args(*k, **kw):
    for jsonfile in get_args().json:
        with open(jsonfile) as openfile:
            json.load(openfile)
    for option in get_args().option:
        l = option.split('=')
        if len(l) == 2:
            name = l[0]
            value = l[1]
            #if usi.api.parameter.exists(name):
            usi.api.parameter.write(name, value)
            #else:
            #    print "Option does not exist: %s" % (name)
            #    sys.exit(1)
        else:
            print "Option malformated '%s', it needs to be formated 'key=value'" % option
            sys.exit(1)

@usi.on("end_of_initialization")
def show_configuration(*k, **kw):
    """View detailed model configuration and check for mal formated options"""
    malformated = False
    for option in get_args().option:
        l = option.split('=')
        if len(l) == 2:
            name = l[0]
            value = l[1]
            if not usi.api.parameter.exists(name):
                print "Option does not exist: %s" % (name)
                malformated = True
    if malformated:
        print "The execution is stoped due to malformated options"
        sys.exit(1)

    if get_args().list:
        print "Parameter List:"
        params = usi.api.parameter.readPropertyDict()
        usi.api.parameter.printDict(params)
        #params = usi.api.parameter.filterDict(params, "generics")
        sys.exit(0)
