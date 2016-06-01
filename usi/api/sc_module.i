// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file sc_module.i
///
/// @date 2016
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module sc_module

%include "std_string.i"
%include "std_vector.i"
%include "usi.i"

USI_REGISTER_MODULE(sc_module)

sc_core::sc_object *create_sc_module(PyObject *cls, PyObject *args, PyObject *kw);

%{

#include "usi/core/module.h"

class sc_module_ : public sc_core::sc_module {
  public:
    sc_module_(sc_core::sc_module_name mn, PyObject *cls, PyObject *args, PyObject *kw):
      sc_core::sc_module(mn), m_cls(cls), m_inst(NULL) {
      Py_INCREF(m_cls);
      m_inst = PyObject_Call(cls, args, kw);
      if(PyErr_Occurred() || !m_inst) {
        PyErr_Print();
      }
      Py_INCREF(m_inst);
    }
    virtual ~sc_module_() {
      Py_XDECREF(m_cls);
      Py_XDECREF(m_inst);
    }

    virtual void start_of_elaboration() {
        run("start_of_elaboration");
    }

    virtual void end_of_elaboration() {
        run("end_of_elaboration");
    }

    virtual void start_of_simulation() {
        run("start_of_simulation");
    }

    virtual void end_of_simulation() {
        run("end_of_simulation");
    }

    void run(const char *name, PyObject *args = NULL, PyObject *kwargs = NULL) {
      PythonModule::globalInstance->block_threads();
      static PyObject *static_args = PyTuple_New(0);
      if(!args) {
        args = static_args;
      }

      // get the callable Python object
      if(m_inst) {
        if(PyObject_HasAttrString(m_inst, name)) {
          PyObject *function = PyObject_GetAttrString(m_inst, name);
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
        }
      }
      PythonModule::globalInstance->unblock_threads();
    }

    static USIObject find(sc_core::sc_object *obj, std::string name) {
      sc_module_ *instance = dynamic_cast<sc_module_ *>(obj);
      if(obj && instance) {
        return instance->m_inst;
      } else {
        return NULL;
      }
    }

  private:
    PyObject *m_cls;
    PyObject *m_inst;
};

sc_core::sc_object *create_sc_module(PyObject *cls, PyObject *args, PyObject *kw) {
  if(PyTuple_Size(args)<1 || !PyString_Check(PyTuple_GetItem(args, 0))) {
    std::cerr << "USI create_sc_module: function takes at least one argument: the sc_module_name" << std::endl;
  }
  return new sc_module_(sc_core::sc_module_name(PyString_AsString(PyTuple_GetItem(args, 0))), cls, args, kw);
}

USIObject find_sc_module(sc_core::sc_object *obj, std::string name) {
  return sc_module_::find(obj, name);
}

USI_REGISTER_OBJECT_GENERATOR(find_sc_module);

%}
