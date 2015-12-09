// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file usi.h
/// @date 2013-2015
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
/// This file renames the python systemc function names to usi function names.
/// It is the main header file for the usi bindings.
/// Include it from the main simulation routine to access the Python USI implementation.
/// Util APIs should import the usi.i from SWIG. It will import all neccecary headers as well
/// but furthermore set up the SWIG environment.
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
