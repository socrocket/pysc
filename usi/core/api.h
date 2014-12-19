// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file api.h
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer 
#ifndef PYSC_USI_CORE_API_H_
#define PYSC_USI_CORE_API_H_

#include <Python.h>

typedef PyObject * PyScObject;

void pysc_init(int argc, char *argv[]);
void pysc_load(const char *module);
void pysc_start_of_initialization();
void pysc_start();
void pysc_signal_handler(int sig);

#endif  // PYSC_USI_CORE_API_H_
/// @}

