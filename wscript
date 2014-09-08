#! /usr/bin/env python
# vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 filetype=python :
top = '..'
REPOSITORY_PATH = "pysc"
REPOSITORY_NAME = "Python SystemC Integration"
REPOSITORY_DESC = """This repository exports a Python SystemC integration for Analysis and Configuration purposes."""
REPOSITORY_TOOLS = [
  "shell",
  "virtualenv"
]

def build(self):
  self.recurse_all()
  self.recurse_all_tests()
