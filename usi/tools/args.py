import argparse
import usi
from usi import usage

ARGS = None
parser = argparse.ArgumentParser(
  usage=usage.USAGE,
  description=usage.HELP,
)

def get_args():
  global ARGS
  if not ARGS:
      ARGS = parser.parse_args()
  return ARGS

parser.add_argument('--credits', dest='credits', action='store_true', help='Show credits')
parser.add_argument('--license', dest='license', action='store_true', help='Show license information')
parser.add_argument('--copyright', dest='copyright', action='store_true', help='Show copyright information')

@usi.on("start_of_initialization")
def args(*k, **kw):
  get_args()

  if ARGS.credits:
      print usage.CREDITS
      sys.exit()

  if ARGS.license:
      print usage.LICENSE
      sys.exit()

  if ARGS.copyright:
      print usage.COPYRIGHT
      sys.exit()

