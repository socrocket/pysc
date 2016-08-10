#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set expandtab:ts=4:sw=4:setfiletype python
import os, sys
import subprocess
from waflib.TaskGen import taskgen_method
from waflib.Errors import ConfigurationError
from waflib import Context
from waflib import Task
from waflib import TaskGen
from waflib import Utils
from common import conf
from datetime import datetime


def symlink(src, dst):
    if sys.platform == "win32":
        # Scheisse
        flags = 1 if os.path.isdir(src) else 0
        import ctypes
        kdll = ctypes.windll.kernel32
        kdll.CreateSymbolicLinkW(unicode(src), unicode(dst), flags)
    else:
        os.symlink(src, dst)


def options(self):
  pass

"""
    # Makes existing virtual env relocatable (for installation?)
    self.cmd_and_log(
        [self.env.VIRTUALENV, "--relocatable", self.env.VENV_PATH],
        output=Context.BOTH,
        cwd=self.bldnode.abspath()
    )
"""
def python_get(self, name):
    self.start_msg("Install %s into virtualenv" % (name))
    self.cmd_and_log(
        [Utils.subst_vars('${VPIP}',self.env), "install", name],
        output=Context.BOTH,
        cwd=self.env.VENV_PATH
    )
    self.end_msg("ok")
conf(python_get)

class venv_link(Task.Task):
  """Link a Python source directory into the site-packages dir of the venv"""
  name = 'venv_link'
  color = 'BLUE'

  def __str__(self):
      return "venv: %s -> virtualenv" % (os.path.basename(self.generator.path.get_bld().abspath()))

  def run(self):
      sdirnode = self.generator.path.get_bld()
      sdirnode.mkdir()
      for snode in self.inputs:
          if os.path.exists(snode.abspath()):
              dnode = snode.get_bld()
              if not os.path.isdir(dnode.parent.abspath()):
                  dnode.parent.mkdir()
              if not os.path.exists(dnode.abspath()):
                  symlink(os.path.relpath(snode.abspath(), os.path.join(dnode.abspath(), "..")), dnode.abspath())
      initnode = sdirnode.find_or_declare('__init__.py')
      if not os.path.exists(initnode.abspath()):
          initnode.write("")
      snode = sdirnode.abspath()
      dnode = os.path.join(self.env["VENV_PATH"], "lib", ("python%s" % self.env.PYTHON_VERSION), "site-packages", os.path.basename(snode))
      if not os.path.exists(dnode) and not os.path.islink(dnode):
          symlink(os.path.relpath(snode, os.path.join(dnode, "..")), dnode)
      self.outputs[0].write(str(datetime.now()))
      return 0

@TaskGen.before('process_source', 'process_rule')
@TaskGen.feature('venv_package')
def venv_package(self):
    srclist = []
    for src in Utils.to_list(getattr(self, "pysource", [])):
        if isinstance(src, str):
            snode = self.path.find_node(src)
        else:
            snode = src
        srclist.append(snode)
    self.env["VENV_PATH"] = os.path.join(self.bld.bldnode.abspath(), ".conf_check_venv")
    snode = self.path.abspath()
    dnode = self.bld.bldnode.find_or_declare(os.path.join(".conf_check_venv", "lib", ("python%s" % self.env.PYTHON_VERSION), "site-packages", os.path.basename(snode)+".waf-info"))
    links = self.create_task('venv_link', src=srclist, tgt=[dnode])

def configure(self):
    try:
        if sys.version_info >= (3, 0):
            self.find_program(['virtualenv', 'virtualenv.py', 'virtualenv.exe'], var="VIRTUALENV", mandatory=True, okmsg="ok")
        else:
            self.find_program(['virtualenv2', 'virtualenv2.py', 'virtualenv2.exe', 'virtualenv', 'virtualenv.py', 'virtualenv.exe'], var="VIRTUALENV", mandatory=True, okmsg="ok")
    except ConfigurationError as e:
        name    = "virtualenv"
        version = "trunk"
        self.dep_fetch(
          name    = name,
          version = version,
          git_url = "https://github.com/pypa/virtualenv.git",
        )
        self.find_program(['virtualenv', 'virtualenv.py', 'virtualenv.exe'], var="VIRTUALENV", mandatory=True, okmsg="ok", path_list=[self.dep_path(name, version)])
    self.start_msg("Create python virtualenv")
    self.env["VENV_PATH"] = os.path.join(self.bldnode.abspath(), ".conf_check_venv")
    self.cmd_and_log(
        [Utils.subst_vars('${VIRTUALENV}',self.env), "-p", sys.executable, self.env.VENV_PATH],
        output=Context.BOTH,
        cwd=self.bldnode.abspath()
    )
    self.end_msg("ok")
    self.find_program('python', var="VPYTHON", mandatory=True, okmsg="ok", path_list=[os.path.join(self.env.VENV_PATH, "bin")])
    self.find_program('pip', var="VPIP", mandatory=True, okmsg="ok", path_list=[os.path.join(self.env.VENV_PATH, "bin")])

