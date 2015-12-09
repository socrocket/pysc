from __future__ import print_function
from builtins import range
from builtins import object
import usi
import os
import pandas as pd
import warnings

logger = None

class Logger(object):
  def __init__(self, log_file):
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      if os.path.exists(log_file):
        os.remove(log_file)
      self.store = pd.HDFStore(log_file, complevel=9, complib='blosc',
          format='table')
      self.msg_buffer = []
      self.columns = []
      self.index = 0
      self.chunk_a = 0

  def log(self, message):
    self.msg_buffer.append(message)
    if len(self.msg_buffer) > 50000:
      self.store_buffer()

  def store_buffer(self):
    with warnings.catch_warnings():
      warnings.simplefilter("ignore")
      if len(self.msg_buffer) > 0:
        # create continous index
        index_col = list(range(self.index, self.index + len(self.msg_buffer)))
        self.index += len(self.msg_buffer)

        df = pd.DataFrame(self.msg_buffer, index=index_col)

        # convert bool columns into str to avoid mixed column exception
        for column in df.columns:
          if df[column].dtype == 'object':
            df[column] = df[column].astype(str)

        # store buffer and free
        self.store.append("log{0}".format(self.chunk_a), df, min_itemsize=250, index=False, data_columns=True)
        self.store.close()
        self.store.open()
        #self.store.create_table_index("log%d" % self.chunk_a, kind="full")

        self.msg_buffer = []
        self.chunk_a += 1

  def __del__(self):
    print("destructor logger")
    if hasattr(self, "store"):
      self.store_buffer()
      self.store.close()

@usi.on("end_of_evaluation")
def save_db(phase):
    global logger
    if logger:
        logger.store_buffer()

def report(
    message_type=None,
    message_text=None,
    severity=None,
    file_name=None,
    line_number=None,
    time=None,
    delta_count=None,
    process_name=None,
    verbosity=None,
    what=None,
    actions=None,
    phase=None,
    **kwargs):
  global logger

  severity_text = ["Info", "Warning", "Error", "Fatal"]

  message_dict = {
      "message_type" : message_type,
      "message_text" : message_text,
      "severity" : severity,
      "file_name" : file_name,
      "line_number" : line_number,
      "time" : time,
      "delta_count" : delta_count,
      "process_name" : process_name,
      "verbosity" : verbosity,
      "what" : what,
      "actions" : actions,
      "phase" : phase,
      }

  message_dict = dict(list(message_dict.items()) + list(kwargs.items()))

  if logger is None:
    logger = Logger("log.h5")
  logger.log(message_dict)
