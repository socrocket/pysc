// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file systemc.h
/// 
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author 
///
#ifndef PYSC_API_SYSTEMC_H
#define PYSC_API_SYSTEMC_H

#include <Python.h>
#include "common/sc_api.h"

#ifdef SWIG
namespace sc_core {
  enum sc_time_unit {SC_FS, SC_PS, SC_NS, SC_US, SC_MS, SC_SEC};
}
#endif

namespace pysc {
namespace api {
namespace systemc {

void set_current_event(const sc_core::sc_event *e);
void event_bind(PyObject* e, PyObject* obj=0);
bool event_notify(PyObject* e);
bool event_notify(PyObject* e, double time, sc_core::sc_time_unit tu=sc_core::SC_NS);
void event_remove(PyObject* e);

void start();
void start(double time, sc_core::sc_time_unit tu);

void stop();

void pause();

void wait(double time, sc_core::sc_time_unit tu);
//void wait(PyObject* e);
//
double simulation_time(sc_core::sc_time_unit tu);
double delta_count();

long get_curr_process_handle();
bool is_running();
//void print_sc_splash();

};
};
}; // pysc

#endif // PYSC_API_SYSTEMC_H
/// @}
