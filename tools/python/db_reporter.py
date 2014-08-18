import pysc
import os
import pandas as pd

logger = None

class Logger():
  def __init__(self, log_file):
    if os.path.exists(log_file):
      os.remove(log_file)
    self.store = pd.HDFStore(log_file, complevel=9, complib='blosc')
    self.msg_buffer = []
    self.columns = []
    self.index = 0
    self.chunk = 0

  def log(self, message):
    self.msg_buffer.append(message)
    if len(self.msg_buffer) > 50000:
      self.store_buffer()

  def store_buffer(self):
    if len(self.msg_buffer) > 0:
      # create continous index
      index_col = range(self.index, self.index + len(self.msg_buffer))
      self.index += len(self.msg_buffer)
      #print range(self.index, len(df["index"]))

      df = pd.DataFrame(self.msg_buffer, index=index_col)

      # convert bool columns into str to avoid mixed column exception
      for column in df.columns:
        if df[column].dtype == 'object':
          df[column] = df[column].astype(str)
      
      # store buffer and free
      self.store.append("log%d" % self.chunk, df, min_itemsize=250, index=False, data_columns=True)
      self.store.create_table_index("log%d" % self.chunk, kind="full")
      
      self.msg_buffer = []
      self.chunk += 1

  def __del__(self):
    print "destructor logger"
    if hasattr(self, "store"):
      self.store_buffer()
      self.store.close()

@pysc.on("end_of_evaluation")
def save_db(phase):
  global logger
  logger.store_buffer()

@pysc.on("report")
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

  message_dict = dict(message_dict.items() + kwargs.items())

  if logger is None:
    logger = Logger("log.h5")

  logger.log(message_dict)
