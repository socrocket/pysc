from __future__ import print_function
import usi
import json
from termcolor import colored

SEVERITY = [
    colored('Info', 'green'),
    colored('Warning', 'yellow'),
    colored('Error', 'red'),
    colored('Fatal', 'red')
]

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
    global SEVERITY

    parameters = ""
    for value in kwargs:
        if isinstance(kwargs[value], int):
            parameters += "{0}={1:#x} ".format(value, kwargs[value])
        else:
            parameters += "{0}={1} ".format(value, kwargs[value])


    print("@{0} ns /{1} ({2}): {3}: {4} {5}".format(time,
          delta_count,
          colored(message_type, 'blue'),
          SEVERITY[severity],
          message_text,
          parameters))

