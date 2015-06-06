#! /usr/bin/env python
# vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 filetype=python :
top = '..'
REPOSITORY_PATH = "pysc"
REPOSITORY_NAME = "Python implementation of the Universal SystemC Scripting Interface"
REPOSITORY_DESC = """This repository exports a Python SystemC integration for Analysis and Configuration purposes."""
REPOSITORY_TOOLS = [
#  "blas",
#  "lapack",
  "virtualenv",
#  "consolelog",
  "shell",
]

def build(self):
    self.recurse_all()
