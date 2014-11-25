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
    //PyEval_InitThreads();
    module_thread = PyThreadState_Get();
    if(funct) {
        funct();
    }
}

/// @}
