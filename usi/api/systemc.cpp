// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file systemc.cpp
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
#include <Python.h>
#include <map>
#include "usi.h"
#include "usi/api/systemc.h"

USI_REGISTER_MODULE(systemc);

namespace pysc {
namespace api {
namespace systemc {

void start() {
  // must be in the kernel thread on entry.  Exit it so we
  // know that no thread is active on entry to any other function
  // called by the kernel
  sc_core::sc_start();
  // re-acquire thread before returning control to Python
}

void start(double time, sc_core::sc_time_unit tu) {
  // must be in the kernel thread on entry.  Exit it so we
  // know that no thread is active on entry to any other function
  // called by the kernel
  sc_core::sc_start(sc_core::sc_time(time, tu));
  // re-acquire thread before returning control to Python
}

void stop() {
  sc_core::sc_stop();
}

void pause() {
  sc_core::sc_pause();
}

void wait(double time, sc_core::sc_time_unit tu) {
  // relinquish thread lock and set current thread to NULL
  PyThreadState *_save = PyEval_SaveThread();
  sc_core::wait(time, tu);
  // now re-establish the previous thread
  PyEval_RestoreThread(_save);
}

double simulation_time(sc_core::sc_time_unit tu) {
  return sc_core::sc_time_stamp().to_seconds() / sc_core::sc_time(1,tu).to_seconds();
}

double delta_count() {
  return sc_core::sc_delta_count();
}

int set_verbosity(int verbosity) {
  return sc_core::sc_report_handler::set_verbosity_level(verbosity);
}

size_t get_curr_process_handle() {
#if SYSTEMC_API == 210
  return (size_t) sc_core::sc_get_curr_process_handle();
#elif SYSTEMC_API == 220 || SYSTEMC_API == 230 || SYSTEMC_API == 231
  return (size_t) sc_core::sc_get_curr_simcontext()->get_curr_proc_info()->process_handle;
#else
#error Unknown SystemC API to call for sc_get_current_process_handle
  return 0;
#endif
}

// Function: gsp_sc_is_running
bool is_running() {
#if SYSTEMC_API == 210
  return sc_core::sc_get_curr_simcontext()->is_running();
#elif SYSTEMC_API == 220 || SYSTEMC_API == 230 || SYSTEMC_API == 231
  return sc_core::sc_is_running();
#else
#error Unknown SystemC API to call for sc_is_running
  return false;
#endif
}

std::vector<sc_core::sc_object *> get_top_level_objects() {
  return sc_core::sc_get_top_level_objects();
}

}; // systemc
}; // api
}; // pysc
/// @}
