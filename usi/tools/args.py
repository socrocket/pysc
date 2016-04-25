from __future__ import print_function
import argparse
import sys
import usi
from usi import usage
from . import execute

ARGS = None
parser = argparse.ArgumentParser(
  usage=usage.USAGE,
  description=usage.HELP,
)

execute.argparse_init(parser)

def include_scripts():
    param = ['-s', '--script']
    args = [arg for idx, arg in enumerate(sys.argv) if arg in param or ( idx > 0 and sys.argv[idx-1] in param)]
    return args

def get_args():
  global ARGS
  if not ARGS:
      args = parser.parse_args(include_scripts())
      execute.argparse_before_parse(args)
      ARGS = parser.parse_args()
  return ARGS

parser.add_argument('--credits', dest='credits', action='store_true', help='Show credits')
parser.add_argument('--license', dest='license', action='store_true', help='Show license information')
parser.add_argument('--copyright', dest='copyright', action='store_true', help='Show copyright information')

@usi.on("start_of_initialization")
def args(*k, **kw):
  get_args()

  if ARGS.credits:
      print(usage.CREDITS)
      sys.exit()

  if ARGS.license:
      print(usage.LICENSE)
      sys.exit()

  if ARGS.copyright:
      print(usage.COPYRIGHT)
      sys.exit()

