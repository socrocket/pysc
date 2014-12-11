import argparse
import usi
from tools.python import usage

ARGS = None
parser = argparse.ArgumentParser(
  usage=usage.USAGE,
  description=usage.HELP,
)

parser.add_argument('--credits', dest='credits', action='store_true', help='Show credits')
parser.add_argument('--license', dest='license', action='store_true', help='Show license information')
parser.add_argument('--copyright', dest='copyright', action='store_true', help='Show copyright information')

@usi.on("start_of_initialization")
def args(*k, **kw):
  global ARGS
  if not ARGS:
      ARGS = parser.parse_args()

  if ARGS.credits:
      print usage.CREDITS
      sys.exit()

  if ARGS.license:
      print usage.LICENSE
      sys.exit()

  if ARGS.copyright:
      print usage.COPYRIGHT
      sys.exit()

  return ARGS
