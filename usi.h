#ifndef USI_H
#define USI_H

#include "usi/core/registry.h"
#include "usi/core/module.h"
#include "usi/core/api.h"
#include <systemc>

#ifndef usi_init
#define usi_init pysc_init
#endif

#ifndef usi_load
#define usi_load pysc_load
#endif

#ifndef usi_start_of_initialization
#define usi_start_of_initialization pysc_start_of_initialization
#endif

#ifndef usi_end_of_initialization
#define usi_end_of_initialization pysc_end_of_initialization
#endif

#ifndef usi_start
#define usi_start pysc_start
#endif

#ifndef USI_INIT_MODULES
#define USI_INIT_MODULES PYSC_INIT_MODULES
#endif

#ifndef USI_HAS_MODULE
#define USI_HAS_MODULE(module) PYSC_HAS_MODULE(module)
#endif

#ifndef USI_REGISTER_MODULE
#define USI_REGISTER_MODULE(module) PYSC_REGISTER_MODULE(module)
#endif

#ifndef USI_REGISTER_OBJECT_GENERATOR
#define USI_REGISTER_OBJECT_GENERATOR(if) PYSC_REGISTER_OBJECT_GENERATOR(if)
#endif

#ifndef USI_REGISTER_OBJECT
#define USI_REGISTER_OBJECT(if) PYSC_REGISTER_OBJECT(if)
#endif

typedef PyScObject USIObject;

#endif  // USI_H
