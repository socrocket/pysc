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

PyScModule *PyScModule::reg = NULL;

PyScModule::PyScModule(PyScModule::init_f funct) : funct(funct) {
  next = reg;
  reg = this;
};

void PyScModule::registerEmbedded() {
  PyScModule *mod = reg;
  while(mod) {
    mod->initModule();
    mod = mod->next;
  }
}

void PyScModule::initModule() {
  PyEval_InitThreads();
  module_thread = PyThreadState_Get();
  if(funct) {
    funct();
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
  while(gen) {
    PyObject *pyobj = gen->funct(obj, obj->name());
    if(pyobj) {
      objs.push_back(pyobj);
    }
    gen = gen->next;
  }
  
  result = PyTuple_New(objs.size());
  for(std::vector<PyObject *>::iterator iter = objs.begin(); iter != objs.end(); ++iter, ++i) {
    PyTuple_SetItem(result, i, *iter);
  }

  return result;
}

PyObject *PyScObjectGenerator::find_object_by_name(std::string name) {
  return PyScObjectGenerator::find_object_by_ptr(sc_find_by_name(name.c_str()));
}

/// @}
