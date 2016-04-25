// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file registry.cpp
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
#include "usi/core/registry.h"
#include "core/common/sc_find.h"
#ifndef NC_SYSTEMC
#include "core/common/sr_param.h"
#endif

#include <Python.h>

PyScModule *PyScModule::reg = NULL;

PyScModule::PyScModule(const char *name, PyScModule::init_f funct) : funct(funct), name(name) {
  next = reg;
  reg = this;
};

PyScModule::operator PyInterpreterState*() {
  return module_thread->interp;
}

void PyScModule::registerEmbedded() {
#if PY_VERSION_HEX >= 0x03000000
  PyScModule *mod = reg;
  while(mod) {
    mod->initModule();
    mod = mod->next;
  }
#endif
}

void PyScModule::prepareEmbedded() {
#if PY_VERSION_HEX < 0x03000000
  PyScModule *mod = reg;
  while(mod) {
    mod->initModule();
    mod = mod->next;
  }
#endif
}


void PyScModule::initModule() {
  if(funct) {
#if PY_VERSION_HEX >= 0x03000000
    PyImport_AppendInittab(name, funct);
#else
    funct();
#endif
  }
}

PyScObjectGenerator *PyScObjectGenerator::reg = NULL;

PyScObjectGenerator::PyScObjectGenerator(PyScObjectGenerator::generator_f funct) : funct(funct) {
    next = reg;
    reg = this;
};

PyObject *PyScObjectGenerator::find_object_by_ptr(sc_core::sc_object *obj) {
  int i = 0;
  PyObject *result = NULL;
  std::vector<PyObject *> objs;

  PyScObjectGenerator *gen = PyScObjectGenerator::reg;
  if(obj) {
    while(gen) {
      PyObject *pyobj = gen->funct(obj, obj->name());
      if(pyobj) {
        objs.push_back(pyobj);
      }
      gen = gen->next;
    }
  }

  result = PyTuple_New(objs.size());
  for(std::vector<PyObject *>::iterator iter = objs.begin(); iter != objs.end(); ++iter, ++i) {
    PyTuple_SetItem(result, i, *iter);
  }

  return result;
}

sc_core::sc_object *PyScObjectGenerator::find_object_by_name(std::string name) {
#ifndef NC_SYSTEMC
  gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
  if(configAPI) {
    gs::cnf::gs_param_base *param = configAPI->getPar(name);
    if(param) {
      return param;
    }
  }
#endif
  return sc_find_by_name(name.c_str());
}

/// @}
