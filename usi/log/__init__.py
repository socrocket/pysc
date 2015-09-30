from __future__ import print_function
import sys
import usi
from usi.tools.args import parser, get_args
from . import console_reporter
from . import db_reporter

REPORT = console_reporter.report

parser.add_argument('-r', '--reporter', dest='reporter', action='store', default='console', type=str, help='Changes the backend for the reporter: console (default) or hdf5=<path>')
parser.add_argument('-v', '--verbosity', dest='verbosity', action='store', default=500, type=int, help='Changes the report verbosity')

@usi.on('start_of_initialization')
def start_of_initialization(phase):
    global REPORT
    reporter = get_args().reporter
    verbosity = get_args().verbosity
    filename = None
    if reporter.startswith("hdf5="):
        filename = reporter[5:]
        db_reporter.logger = db_reporter.Logger(filename)
        REPORT = db_reporter.report
    elif reporter == "console":
        REPORT = console_reporter.report
    else:
        print("Reporter unknown '%s'" % reporter)
        sys.exit(1)
    usi.on("report")(REPORT)

    print("Set verbosity to level %d" % verbosity)
    print("Old verbosity level was %d" % usi.set_verbosity(verbosity))

