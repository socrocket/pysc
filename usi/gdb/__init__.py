
def debug_simulation():
  import os
  import tmuxp
  #import usi.shell
  server = tmuxp.Server()
  session = server.sessions[0]
  window = session.new_window(window_name="GDB Simulation")
  #usi.shell.stop()
  window.pane[0].send_keys("gdb program %s" % os.getpid())



