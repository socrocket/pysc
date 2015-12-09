from builtins import object
import pandas as pd
import re

class LogQuery(object):
  """
  Class for reading SoCRocket logs from HDF5-databases

  Example:

  import pandas as pd
  import log_query as lq

  log = lq.LogQuery("log.h5")
  df = log.select(where="index >= -1", columns=['index', 'time', 'message_text'])
  print df
  log.close_file()
  """
  def __init__(self, logfile):
    self.store = pd.HDFStore(logfile)
    self.keys = []
    for key in list(self.store.keys()):
      if re.match(r"/log\d+", key):
        self.keys.append(key)

  def close_file(self):
    self.store.close()
    pass

  def select(self, **kwargs):
    result = pd.DataFrame()
    for key in self.keys:
      try:
        result = result.append(self.store.select(key, **kwargs))
      except ValueError:
        pass
    return result

