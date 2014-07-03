// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file pysc.cpp
/// 
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author 
///
#include <Python.h>
// SystemC library
#include <systemc>
#include <cstdlib>
#include <cstring>
#include <cstdio>

#include "pysc/pysc.h"
#include "pysc/module.h"


PythonModule *PythonModule::globalInstance = NULL;

// two functions to allow OS-independent operation of load()
std::string PythonModule::path_separator() {
  #ifdef MS_WINDOWS
    return std::string("\\"};
  #else
    return std::string("/");
  #endif
}

bool PythonModule::is_simple_filename(const char *path) {
  #ifdef MS_WINDOWS
    // relative to current directory
    if(*path == '.') return false;
    // absolute
    if((*path >= 'a') && (*path <= 'z') && (path[1] == ':')) return false;
    if((*path >= 'A') && (*path <= 'Z') && (path[1] == ':')) return false;
    if(*path == '\\') return false;
    return true;
  #else  // UNIX-style filesystem paths
    // relative to current directory
    if(*path == '.') return false;
    // absolute
    if(*path == '/') return false;
    return true;
  #endif
}

// constructor
PythonModule::PythonModule(
  sc_core::sc_module_name name_p, char* script_filename,
  int argc, char **argv) :
  sc_core::sc_module(name_p), initialised(false),
  my_namespace(NULL), pysc_module(NULL), sys_path(NULL), name_py(NULL) {

  // set up interpreter and gs module and context object
  subscribe();
  block_threads();

  Py_SetProgramName(argv[0]);
  char *args[argc];
  args[0] = (char *)script_filename;
  for(int i = 1; i< argc; i++) {
      args[i] = argv[i];
  }
  PySys_SetArgvEx(argc, args, 0);

  PyScIncludeModule(pysystemc);
  PyScIncludeModule(pygc);
  PyScRegisterEmbeddedModules();

  // get a globals() dict for this PythonModule
  PyObject* main_module = PyImport_AddModule("__main__");  // borrowed ref
  if(!main_module) {
      PyErr_Print();
      unblock_threads();
      return;
  }
  my_namespace = PyModule_GetDict(main_module);  // borrowed ref
  my_namespace = PyDict_Copy(my_namespace);  // new ref

  // make sure there's a reference to the gs module available
  pysc_module = PyImport_ImportModuleEx(const_cast<char *>("pysc"), my_namespace, my_namespace, NULL);
  if(!pysc_module) {
      PyErr_Print();
      unblock_threads();
      return;
  }

  // get a ref to sys.path
  // note that we do this once only.  if sys.path is ever assigned to a
  // new object, subsequent load()s/add-to-path()s will use the original
  // but imports will use the new
  PyObject *sys = PyImport_ImportModuleEx(const_cast<char *>("sys"), my_namespace, my_namespace, NULL);
  if(!sys) {
      PyErr_Print();
      unblock_threads();
      return;
  }
  Py_XDECREF(sys);

  sys_path = PyObject_GetAttrString(sys, "path");  // new ref
  if(!sys_path) {
      PyErr_Print();
      unblock_threads();
      return;
  }

  initialised = true;
  // if we get to here, we consider ourselves initialised
  // note that:
  // - the namespace has no name, so is impossible to access from another PythonModule
  // - pysc and sys have been imported, but are not added to the namespace

  // tell the Python code it is embedded
  PyObject_SetAttrString(pysc_module, "__standalone__", Py_False);

  // tell the Python code its interpreter name
  name_py = PyString_FromString(name());  // new ref
  set_interpreter_name();

  unblock_threads();

  add_to_pythonpath(".");

  PythonModule::globalInstance = this;

  // run a script if one has been requested
  if (script_filename && *script_filename) {
    execfile(script_filename);
  }
}

// desctructor
PythonModule::~PythonModule() {
  Py_XDECREF(my_namespace);
  my_namespace = NULL;
  Py_XDECREF(pysc_module);
  pysc_module = NULL;
  Py_XDECREF(sys_path);
  sys_path = NULL;
  Py_XDECREF(name_py);
  name_py = NULL;
  unsubscribe();
}

// public load function - runs a Python file in a module-specific
// namespace.  searches for the file in the PYTHONPATH unless it
// is an absolute pathname or starts wth a '.'
void PythonModule::execfile(const char* script_filename) {
  if(!initialised) {
    return;
  }
  block_threads();
  // Load the script, trying the python path first, then the CWD
  // Go direct to the CWD if an absolute or relative path is given
  // rather than a simple filename
  if(is_simple_filename(script_filename)) {
    int path_size = PyList_Size(sys_path);
    for(int i=0; i<path_size; i++) {
      PyObject *path_py = PyList_GetItem(sys_path, i);  // borrowed ref
      std::string s(PyString_AsString(path_py));
      s += path_separator() + std::string(script_filename);
      if(private_load(s.c_str())) {
        unblock_threads();
        return;
      }
    }
  }
  if(!private_load(script_filename)) {
    std::string s(name());
    s += std::string(" could not find ") + std::string(script_filename);
    perror(s.c_str());
  }
  unblock_threads();
}


void PythonModule::exec(const char* statement) {
  if(!initialised) {
    return;
  }
  block_threads();

  set_interpreter_name();

  // run the command
  PyObject *ret = PyRun_String(
    statement, Py_single_input, my_namespace, my_namespace);
  if(ret == NULL) PyErr_Print();
  Py_XDECREF(ret);

  unblock_threads();
}

void PythonModule::add_to_pythonpath(const char* path) {
  if(!initialised) {
    return;
  }
  block_threads();
  PyObject *path_py = PyString_FromString(path);
  if(PyList_Insert(sys_path, 0, path_py) < 0) {
    PyErr_Print();
  }
  Py_XDECREF(path_py);
  unblock_threads();
}

bool PythonModule::private_load(const char *fullname) {
  FILE *script = fopen(fullname,"r");
  if(!script) {
    return false;
  }

  set_interpreter_name();

  PyObject *ret = PyRun_File(script, fullname, Py_file_input, my_namespace, my_namespace);
  if(ret == NULL) {
    PyErr_Print();
  }
  Py_XDECREF(ret);

  fclose(script);
  return true;
}

void PythonModule::set_interpreter_name() {
  PyObject_SetAttrString(pysc_module, "__interpreter_name__", name_py);
}

void PythonModule::run_py_callback(const char* name, PyObject *args) {
  if(!initialised) {
    return;
  }
  block_threads();

  set_interpreter_name();

  // get the callable Python object
  PyObject *dict =
    PyObject_GetAttrString(pysc_module, "PHASE");
  if(dict) {
    PyObject *member =
      PyDict_GetItemString(dict, name);

    if(member) {
      PyObject *ret = PyObject_CallObject(member, args);
      if(ret == NULL) {
        PyErr_Print();
      }
      Py_XDECREF(ret);
      Py_XDECREF(member);
    } else {
      PyErr_Print();
    }
    Py_XDECREF(dict);
  } else {
    PyErr_Print();
  }
  unblock_threads();
}

void PythonModule::start_of_initialization() {
  run_py_callback("start_of_initialization");
}

void PythonModule::end_of_initialization() {
  run_py_callback("end_of_initialization");
}

void PythonModule::start_of_elaboration() {
  run_py_callback("start_of_elaboration");
}

void PythonModule::end_of_elaboration() {
  run_py_callback("end_of_elaboration");
}

void PythonModule::start_of_simulation() {
  run_py_callback("start_of_simulation");
}

void PythonModule::end_of_simulation() {
  run_py_callback("end_of_simulation");
}

void PythonModule::start_of_evaluation() {
  run_py_callback("start_of_evaluation");
}

void PythonModule::end_of_evaluation() {
  run_py_callback("end_of_evaluation");
}

// Code for creating a Python virtual machine.
PyThreadState *PythonModule::singleton;
unsigned PythonModule::subscribers = 0;

void PythonModule::block_threads() {
  PyEval_RestoreThread(singleton);
}

void PythonModule::unblock_threads() {
  singleton = PyEval_SaveThread();
}

extern "C" { void init_pysystemc(void); };

void PythonModule::subscribe() {
  if(subscribers==0) {
    // Initialize Python without signal handlers
    Py_InitializeEx(0);
    PyEval_InitThreads();
    unblock_threads();
  }
  subscribers++;
}

void PythonModule::unsubscribe() {
  subscribers--;
  if(subscribers==0) {
    block_threads();
    Py_Finalize();
  }
}

/// @}
