// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file registry.h
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer
#ifndef PYSC_USI_CORE_REGISTRY_H_
#define PYSC_USI_CORE_REGISTRY_H_

#include <Python.h>

class PyScModule {
  public:
    typedef void (*init_f)(void);
    PyScModule(init_f funct = NULL);
    operator PyThreadState*() { return module_thread; };
    operator PyInterpreterState*() { return module_thread->interp; };
    static void registerEmbedded();
    bool embedded;
  private:
    static PyScModule *reg;
    void initModule();

    PyThreadState *module_thread;
    init_f funct;
    PyScModule *next;
};

#define PYSC_REGISTER_MODULE(name) \
  extern "C" { \
    void init_##name(void); \
  }; \
  static PyScModule __pysc_module(init_##name); \
  volatile PyScModule *__pysc_module_##name = &__pysc_module;

#define PYSC_THIS_MODULE() \
  (__pysc_module)

#define PyScThisModule() \
  (__pysc_module)

#define PYSC_INIT_MODULES() \
  PyScModule::registerEmbedded();

#define PYSC_HAS_MODULE(name) \
  extern PyScModule *__pysc_module_##name; \
  __pysc_module_##name->embedded = true;

#endif // PYSC_USI_REGISTRY_H_
/// @}
