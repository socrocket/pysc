from __future__ import print_function
import usi
import ctypes
import json

c_uint32 = ctypes.c_uint32

class ActionFlagBits (ctypes.LittleEndianStructure):
  _fields_ = [
      ("SC_DO_NOTHING", c_uint32, 1),
      ("SC_THROW", c_uint32, 1),
      ("SC_LOG", c_uint32, 1),
      ("SC_DISPLAY", c_uint32, 1),
      ("SC_CACHE_REPORT", c_uint32, 1),
      ("SC_INTERRUPT", c_uint32, 1),
      ("SC_STOP", c_uint32, 1),
      ("SC_ABORT", c_uint32, 1)]

class ActionFlags (ctypes.Union):
  _fields_ = [
      ("b", ActionFlagBits),
      ("raw", c_uint32)]
  _anonymous_ = ("b")

def get_actions_str(actions):
  result = ""

  if actions == 0:
    result = "SC_UNSPECIFIED"
  else:
    flags = ActionFlags()
    flags.raw = actions
    if flags.SC_DO_NOTHING == 1:
      result += "SC_DO_NOTHING|"
    if flags.SC_THROW == 1:
      result += "SC_THROW|"
    if flags.SC_LOG == 1:
      result += "SC_LOG|"
    if flags.SC_DISPLAY == 1:
      result += "SC_DISPLAY|"
    if flags.SC_CACHE_REPORT == 1:
      result += "SC_CACHE_REPORT|"
    if flags.SC_INTERRUPT == 1:
      result += "SC_INTERRUPT|"
    if flags.SC_STOP == 1:
      result += "SC_STOP|"
    if flags.SC_ABORT == 1:
      result += "SC_ABORT|"


  return result[:-1]

@usi.on("report")
def report_full(
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

  print("------------------------------------------------------------------------")
  print("message_type : ", message_type)
  print("message_text : ", message_text)
  print("severity     : ", severity_text[severity])
  print("file_name    : ", file_name)
  print("line_number  : ", line_number)
  print("time         : ", time)
  print("delta_count  : ", delta_count)
  print("process_name : ", process_name)
  print("verbosity    : ", verbosity)
  print("what         : ", what)
  print("actions      : ", get_actions_str(actions))
  print("phase        : ", phase)
  print("parameters   : ", json.dumps(kwargs))
  print("------------------------------------------------------------------------")

