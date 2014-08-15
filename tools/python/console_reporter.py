import pysc
import json

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

  severity_text = ["Info", "Warning", "Error", "Fatal"]
  
  parameters = ""
  for value in kwargs:
    if isinstance(kwargs[value], int) or isinstance(kwargs[value], long):
      parameters += "{0}={1:#x} ".format(value, kwargs[value])
    else:
      parameters += "{0}={1} ".format(value, kwargs[value])

  print "@{0} ps /{1} ({2}): {3}: {4} {5}".format(time, delta_count, message_type,
      severity_text[severity], message_text, parameters)

