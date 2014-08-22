import pysc
import json
from termcolor import colored

@pysc.on("start_of_initialization")
def start_of_initialization(phase):
  verbosity = 500
  pysc.set_verbosity(verbosity)

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

  if severity == 0:
    severity_color = 'green'
  elif severity == 1:
    severity_color = 'yellow'
  else:
    severity_color = 'red'

  print "@{0} ns /{1} ({2}): {3}: {4} {5}".format(time, 
      delta_count,
      colored(message_type, 'blue'),
      colored(severity_text[severity], severity_color), 
      message_text, 
      parameters)

