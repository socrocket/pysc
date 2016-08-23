// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file module.cpp
///
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
///
#include <Python.h>
// SystemC library
#include <systemc>
#include <cstdlib>
#include <string>
#include <cstdio>
#ifndef MTI_SYSTEMC
#include <boost/filesystem.hpp>
#endif
#include <boost/algorithm/string.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <map>
#include <set>

#if not (defined(MTI_SYSTEMC) and defined(NC_SYSTEMC))
#include "core/base/waf.h"
#endif
#include "core/common/sr_report.h"
#include "usi/core/module.h"
#include "usi/core/registry.h"

#define PyString_FromString(x) PyUnicode_FromStringAndSize(x, strlen(x))
PythonModule *PythonModule::globalInstance = NULL;

// constructor
PythonModule::PythonModule(
    sc_core::sc_module_name mn,
    const char* script_filename,
    int argc,
    char **argv) :
        sc_core::sc_module(mn),
        initialised(false),
        my_namespace(NULL),
        pysc_module(NULL),
        sys_path(NULL),
        name_py(NULL) {

    PYSC_INIT_MODULES();

    // set up interpreter and gs module and context object
    subscribe();
    block_threads();

    PYSC_PREPARE_MODULES();

#ifndef MTI_SYSTEMC
#if PY_MAJOR_VERSION >= 3
    wchar_t *args[argc];
    for(int i = 0; i< argc; i++) {
        args[i] = new wchar_t[strlen(argv[i])+1];
        mbstowcs(args[i], argv[i], strlen(argv[i])+1);
    }
    Py_SetProgramName(args[0]);
    if(script_filename && *script_filename) {
      delete args[0];
      args[0] = new wchar_t[strlen(script_filename)+1];
      mbstowcs(args[0], script_filename, strlen(script_filename)+1);
    }
    PySys_SetArgvEx(argc, args, 0);
#else
    char *args[argc];
    for(int i = 0; i< argc; i++) {
        args[i] = argv[i];
    }
    Py_SetProgramName(args[0]);
    if(script_filename && *script_filename) {
      args[0] = const_cast<char *>(script_filename);
    }
    PySys_SetArgvEx(argc, args, 0);
#endif

#else
    Py_SetProgramName("vsim");
    PySys_SetArgvEx(0, NULL, 0);
#endif

    // get a globals() dict for this PythonModule
    PyObject* main_module = PyImport_AddModule("__main__");  // borrowed ref
    if(!main_module) {
        PyErr_Print();
        unblock_threads();
        return;
    }
    my_namespace = PyModule_GetDict(main_module);  // borrowed ref
    my_namespace = PyDict_Copy(my_namespace);  // new ref

    sys_path = PySys_GetObject(const_cast<char *>("path"));  // new ref
    if(!sys_path) {
        PyErr_Print();
        unblock_threads();
        return;
    }

    initialised = true;

    // Now add the virtual env to the sys.path to load pysc and other socrocket modules
    unblock_threads();
#if defined(MTI_SYSTEMC) || defined(NC_SYSTEMC)
    boost::filesystem::path builddir = findPath("build", __FILE__);
#else
    std::map<std::string, std::string> *wafConfig = getWafConfig(argv[0]);
    std::string outdir = (*wafConfig)["out_dir"];
    outdir.erase(std::remove(outdir.begin(), outdir.end(), '\''), outdir.end());
    boost::filesystem::path builddir(outdir);
#endif
    boost::filesystem::path venvactivate(".conf_check_venv/bin/activate_this.py");
    std::string activate = (builddir/venvactivate).string();
    exec(
        "with open('"+activate+"') as script:\n" +
        "    code = compile(script.read(), '"+activate+"', 'exec')\n" +
        "    exec(code, dict(__file__='"+activate+"'))");
    block_threads();

    // make sure there's a reference to the pysc module available
    pysc_module = PyImport_ImportModuleEx(const_cast<char *>("usi"), my_namespace, my_namespace, NULL);
    if(!pysc_module) {
        PyErr_Print();
        unblock_threads();
        return;
    }

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
      load(script_filename);
    }

#ifndef MTI_SYSTEMC
    sr_report_handler::handler = report_handler;
#endif
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

void PythonModule::load(std::string script) {
    if(!initialised) {
        return;
    }
    block_threads();
    if(boost::algorithm::ends_with(script, ".py")) {
        if(!private_load(script.c_str())) {
            std::string s(name());
            s += std::string(" could not load ") + std::string(script);
            perror(s.c_str());
        }
    } else if(PyImport_ImportModuleEx(const_cast<char *>(script.c_str()), my_namespace, my_namespace, NULL)) {
        PyErr_Print();
    }
    unblock_threads();
}


void PythonModule::exec(std::string statement) {
    if(!initialised) {
        return;
    }
    block_threads();

    set_interpreter_name();

    // run the command
    PyObject *ret = PyRun_String(
        statement.c_str(), Py_single_input, my_namespace, my_namespace);
    if(ret == NULL) {
        PyErr_Print();
    }

    Py_XDECREF(ret);

    unblock_threads();
}

void PythonModule::add_to_pythonpath(std::string path) {
  if(!initialised) {
      return;
  }
  block_threads();
  PyObject *path_py = PyString_FromString(path.c_str());
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
      fclose(script);

      return false;
  }
  Py_XDECREF(ret);
  fclose(script);

  return true;
}

void PythonModule::set_interpreter_name() {
    if(pysc_module) {
        PyObject_SetAttrString(pysc_module, "__interpreter_name__", name_py);
    }
}

void PythonModule::run_py_callback(const char *name, PyObject *args, PyObject *kwargs) {
    static PyObject *static_args = PyTuple_New(0);
    if(!initialised) {
        return;
    }
    block_threads();
    set_interpreter_name();

    if(!args) {
      args = static_args;
    }

    // get the callable Python object
    PyObject *dict = PyObject_GetAttrString(pysc_module, "PHASE");
    if(dict) {
      PyObject *member = PyDict_GetItemString(dict, name);
      if(member) {
        PyObject *function = PyObject_GetAttrString(member, "call");
        if(function) {
          PyObject *ret = PyObject_Call(function, args, kwargs);
          if(PyErr_Occurred() || !ret) {
            PyErr_Print();
          } else {
            Py_XDECREF(ret);
          }
          Py_XDECREF(function);
        } else {
          PyErr_Print();
        }
        // Py_XDECREF(member); Borrowed
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

void PythonModule::pause_of_simulation() {
    run_py_callback("pause_of_simulation");
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

void (*PythonModule::signal(int sig, void (*handler)(int)))(int) {
    return PyOS_setsig(sig, handler);
}

// Code for creating a Python virtual machine.
PyThreadState *PythonModule::singleton;
unsigned int PythonModule::subscribers = 0;
unsigned int PythonModule::blocking = 0;

void PythonModule::block_threads() {
    /// @todo: This is not good we shuld think about removing the blocks
    blocking--;
    if(blocking == 0) {
      PyEval_RestoreThread(singleton);
    }
}

void PythonModule::unblock_threads() {
    if(blocking == 0) {
      singleton = PyEval_SaveThread();
    }
    blocking++;
}

void PythonModule::subscribe() {
    if(subscribers==0) {
        // Initialize Python without signal handlers
        Py_InitializeEx(1);
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

const char *str_value(const char *str) {
  return (str&&*str) ? str : "";
}

#ifndef MTI_SYSTEMC
void PythonModule::report_handler(const sc_core::sc_report &rep, const sc_core::sc_actions &actions) {
  block_threads();
  const sr_report *srr = dynamic_cast<const sr_report *>(&rep);
  PyObject *pairs = PyDict_New();
  if(srr) {
    for(std::vector<v::pair>::const_iterator iter = srr->pairs.begin(); iter!=srr->pairs.end(); iter++) {
      PyObject *i = NULL;
      switch(iter->type) {
        case v::pair::INT32:  i = PyLong_FromLong(boost::any_cast<int32_t>(iter->data)); break;
        case v::pair::UINT32: i = PyLong_FromLong(boost::any_cast<uint32_t>(iter->data)); break;
        case v::pair::INT64:  i = PyLong_FromLongLong(boost::any_cast<int64_t>(iter->data)); break;
        case v::pair::UINT64: i = PyLong_FromUnsignedLongLong(boost::any_cast<uint64_t>(iter->data)); break;
        case v::pair::STRING: i = PyString_FromString(boost::any_cast<std::string>(iter->data).c_str()); break;
        case v::pair::BOOL:   i =                   (boost::any_cast<bool>(iter->data))? (Py_INCREF(Py_True), Py_True) : (Py_INCREF(Py_False), Py_False); break;
        case v::pair::DOUBLE: i = PyFloat_FromDouble(boost::any_cast<double>(iter->data)); break;
        case v::pair::TIME:   i = PyFloat_FromDouble(boost::any_cast<sc_core::sc_time>(iter->data).to_default_time_units()); break;
        default:              i = PyLong_FromLong(boost::any_cast<int32_t>(iter->data));
      }
      if(i) {
        PyObject *key = PyUnicode_FromString(iter->name.c_str());
        PyDict_SetItem(pairs, key, i);
        Py_XDECREF(key);
        Py_XDECREF(i);
      } else {
        std::cout << "could not convert to python: " << iter->name << std::endl;
      }
    }
  }

  if(rep.get_severity()==sc_core::SC_MAX_SEVERITY && rep.get_verbosity() == 0x0FFFFFFF && std::strncmp(rep.get_msg(), "command", 8) == 0) {
    PyObject *obj = PyTuple_New(1);
    PyTuple_SetItem(obj, 0, PyString_FromString(str_value(rep.get_msg_type())));
    PythonModule::globalInstance->run_py_callback("command", obj, pairs);
    Py_XDECREF(obj);

  } else {
    PyObject *obj = PyTuple_New(11);
    PyTuple_SetItem(obj, 0, PyString_FromString(str_value(rep.get_msg_type())));
    PyTuple_SetItem(obj, 1, PyString_FromString(str_value(rep.get_msg())));
    PyTuple_SetItem(obj, 2, PyLong_FromLong(rep.get_severity()));
    PyTuple_SetItem(obj, 3, PyString_FromString(str_value(rep.get_file_name())));
    PyTuple_SetItem(obj, 4, PyLong_FromLong(rep.get_line_number()));
    PyTuple_SetItem(obj, 5, PyFloat_FromDouble(rep.get_time().to_default_time_units()));
    PyTuple_SetItem(obj, 6, PyLong_FromLong(sc_core::sc_delta_count()));
    PyTuple_SetItem(obj, 7, PyString_FromString(str_value(rep.get_process_name())));
    PyTuple_SetItem(obj, 8, PyLong_FromLong(rep.get_verbosity()));
    PyTuple_SetItem(obj, 9, PyString_FromString(str_value(rep.what())));
    PyTuple_SetItem(obj, 10, PyLong_FromLong(actions));
    PythonModule::globalInstance->run_py_callback("report", obj, pairs);
    Py_XDECREF(obj);

    //if(actions & (sc_core::SC_STOP | sc_core::SC_ABORT | sc_core::SC_INTERRUPT | sc_core::SC_THROW)) {
    //  sc_core::sc_report_handler::default_handler(rep, actions & ~(sc_core::SC_DISPLAY | sc_core::SC_LOG));
    //}
  }
  Py_XDECREF(pairs);
  unblock_threads();
}
#endif

/// @}
