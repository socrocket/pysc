#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

# <-- removing this magic comment breaks Python 3.4 on Windows
"""
1. Dump binary data to the following text format:

00000000: 00 00 00 5B 68 65 78 64  75 6D 70 5D 00 00 00 00  ...[hexdump]....
00000010: 00 11 22 33 44 55 66 77  88 99 AA BB CC DD EE FF  .."3DUfw........

2. Restore binary data from the formats above as well
   as from less exotic strings of raw hex

"""

__version__ = '3.1'
__author__  = 'anatoly techtonik <techtonik@gmail.com>'
__license__ = 'Public Domain'
__url__ = 'https://bitbucket.org/techtonik/hexdump/'

from builtins import bytes
from builtins import chr
from builtins import range
import binascii  # binascii is required for Python 3
import sys

# --- constants
PY3K = sys.version_info >= (3, 0)

# --- - chunking helpers
def chunks(seq, size):
  '''Generator that cuts sequence (bytes, memoryview, etc.)
     into chunks of given size. If `seq` length is not multiply
     of `size`, the lengh of the last chunk returned will be
     less than requested.

     >>> list( chunks([1,2,3,4,5,6,7], 3) )
     [[1, 2, 3], [4, 5, 6], [7]]
  '''
  d, m = divmod(len(seq), size)
  for i in range(d):
    yield seq[i*size:(i+1)*size]
  if m:
    yield seq[d*size:]

def chunkread(f, size):
  '''Generator that reads from file like object. May return less
     data than requested on the last read.'''
  c = f.read(size)
  while len(c):
    yield c
    c = f.read(size)

def genchunks(mixed, size):
  '''Generator to chunk binary sequences or file like objects.
     The size of the last chunk returned may be less than
     requested.'''
  if hasattr(mixed, 'read'):
    return chunkread(mixed, size)
  else:
    return chunks(mixed, size)
# --- - /chunking helpers


def dehex(hextext):
  """
  Convert from hex string to binary data stripping
  whitespaces from `hextext` if necessary.
  """
  if PY3K:
    return bytes.fromhex(hextext)
  else:
    hextext = "".join(hextext.split())
    return hextext.decode('hex')

def dump(data, binary = False):
  '''
  Convert binary data (bytes in Python 3 and str in
  Python 2) to hex string like '00 DE AD BE EF'.
  '''
  if binary:
    base = '>08b'
  else:
    base = '>02X'

  if PY3K:
    return ' '.join(format(x, base) for x in data)
  else:
    return ' '.join(format(ord(x), base) for x in data)

def dumpgen(data, binary = False):
  '''
  Generator that produces strings:

  '00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................'
  '''
  generator = genchunks(data, 16)
  for addr, d in enumerate(generator):
    # 00000000:
    line = '%08X: ' % (addr*16)
    # 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00
    dumpstr = dump(d, binary)
    if binary:
      line += dumpstr[:8*9]
      if len(d) > 8:  # insert separator if needed
        line += ' ' + dumpstr[8*9:]
    else:
      line += dumpstr[:8*3]
      if len(d) > 8:  # insert separator if needed
        line += ' ' + dumpstr[8*3:]
    # ................
    # calculate indentation, which may be different for the last line
    pad = 2
    if len(d) < 16:
      if binary:
        pad += 9*(16 - len(d))
      else:
        pad += 3*(16 - len(d))
    if len(d) <= 8:
      pad += 1
    line += ' '*pad

    for byte in d:
      # printable ASCII range 0x20 to 0x7E
      if not PY3K:
        byte = ord(byte)
      if 0x20 <= byte <= 0x7E:
        line += chr(byte)
      else:
        line += '.'
    yield line

def dumps(data, result='print', binary=False):
  '''
  Transform binary data to the hex dump text format:

  00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................

    [x] data argument as a binary string
    [x] data argument as a file like object

  Returns result depending on the `result` argument:
    'print'     - prints line by line
    'return'    - returns single string
    'generator' - returns generator that produces lines
  '''
  if PY3K and type(data) == str:
    raise TypeError('Abstract unicode data (expected bytes sequence)')

  gen = dumpgen(data, binary)
  if result == 'generator':
    return gen
  elif result == 'return':
    return '\n'.join(gen)
  elif result == 'print':
    for line in gen:
      print(line)
  else:
    raise ValueError('Unknown value of `result` argument')

def hexloads(dump):
  '''
  Restore binary data from a hex dump.
    [x] dump argument as a string
    [ ] dump argument as a line iterator

  Supported formats:
    [x] hexdump.hexdump
    [x] Scapy
    [x] Far Manager
  '''
  minhexwidth = 2*16    # minimal width of the hex part - 00000... style
  bytehexwidth = 3*16-1 # min width for a bytewise dump - 00 00 ... style

  result = bytes() if PY3K else ''
  if type(dump) != str:
    raise TypeError('Invalid data for restore')

  text = dump.strip()  # ignore surrounding empty lines
  for line in text.split('\n'):
    # strip address part
    addrend = line.find(':')
    if 0 < addrend < minhexwidth:  # : is not in ascii part
      line = line[addrend+1:]
    line = line.lstrip()
    # check dump type
    if line[2] == ' ':  # 00 00 00 ...  type of dump
      # check separator
      sepstart = (2+1)*7+2  # ('00'+' ')*7+'00'
      sep = line[sepstart:sepstart+3]
      if sep[:2] == '  ' and sep[2:] != ' ':  # ...00 00  00 00...
        hexdata = line[:bytehexwidth+1]
      elif sep[2:] == ' ':  # ...00 00 | 00 00...  - Far Manager
        hexdata = line[:sepstart] + line[sepstart+3:bytehexwidth+2]
      else:                 # ...00 00 00 00... - Scapy, no separator
        hexdata = line[:bytehexwidth]
      line = hexdata
    result += dehex(line)
  return result

if __name__ == '__main__':
  from optparse import OptionParser
  parser = OptionParser(usage='''
  %prog binfile
  %prog -b binfile
  %prog -r hexfile''', version=__version__)
  parser.add_option('-r', '--restore', action='store_true', help='restore binary from hex dump')
  parser.add_option('-b', '--binary', action='store_true', help='produces a binary dump of the binfile')

  options, args = parser.parse_args()

  if not args:
    parser.print_help()
    sys.exit(-1)
  else:
    if not options.restore:
      # [x] memory effective dump
      dumps(open(args[0], 'rb'), binary=options.binary)
    else:
      # [ ] memory efficient restore
      # [x] Python works with stdout in text mode by default, which
      #     leads to corrupted binary data on Windows
      #       python -c "import sys; sys.stdout.write('_\n_')" > file
      #       python -c "print(repr(open('file', 'rb').read()))"
      if PY3K:
        sys.stdout.buffer.write(hexloads(open(args[0]).read()))
      else:
        if sys.platform == "win32":
          import os, msvcrt
          msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        sys.stdout.write(hexloads(open(args[0], 'rb').read()))

# [x] file restore from command line utility
# [ ] encoding param for hexdump()ing Python 3 str if anybody requests that

# [ ] document chunking API
# [ ] document hexdump API
