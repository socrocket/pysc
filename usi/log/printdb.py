from __future__ import print_function
from __future__ import absolute_import
import pandas as pd
import log_query as lq
import warnings
import sys

if len(sys.argv) == 1:
  print("Usage: python printdb.py <logfile> <optional PyTables query string>")
  sys.exit()

if len(sys.argv) == 2:
  query = "index > -1"
else:
  query = sys.argv[2]

with warnings.catch_warnings():
  warnings.simplefilter("ignore")
  log = lq.LogQuery(sys.argv[1])
  df = log.select(where=query,
      columns=["index", "time", "message_type", "message_text"])
  for row in df.iterrows():
    print("{0:<4} {1:<15.1f} {2:<35} {3}".format(row[0], row[1]['time'],
        row[1]['message_type'], row[1]['message_text']))
  log.close_file()
