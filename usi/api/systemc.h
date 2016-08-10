// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file systemc.h
///
/// @date 2013-2015
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
#ifndef PYSC_API_SYSTEMC_H
#define PYSC_API_SYSTEMC_H

#include <Python.h>
#include "core/common/sc_api.h"

#ifdef SWIG
namespace sc_core {
  enum sc_time_unit {SC_FS, SC_PS, SC_NS, SC_US, SC_MS, SC_SEC};
}
#endif

namespace pysc {
namespace api {
namespace systemc {

void start();
void start(double time, sc_core::sc_time_unit tu);

void stop();

void pause();

void wait(double time, sc_core::sc_time_unit tu);
double simulation_time(sc_core::sc_time_unit tu);
double delta_count();

int set_verbosity(int verbosity);

size_t get_curr_process_handle();
bool is_running();
std::vector<sc_core::sc_object *> get_top_level_objects();

};
};
}; // pysc

#endif // PYSC_API_SYSTEMC_H
/// @}
