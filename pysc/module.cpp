#include <pysc/module.h>

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

