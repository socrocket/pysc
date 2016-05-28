// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file api.cpp
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer

#include <signal.h>
#include <systemc.h>
#include "usi/core/module.h"

static PythonModule *python = NULL;
void (*cpp_sigint)(int) = NULL;
void (*cpp_sigterm)(int) = NULL;

void pysc_init(int argc, char *argv[]) {
  python = new PythonModule("python_interpreter", NULL, argc, argv);
}

void pysc_load(const char *module) {
  if(python) {
    python->load(module);
  }
}

void pysc_start_of_initialization() {
  python->start_of_initialization();
}

void pysc_end_of_initialization() {
  python->end_of_initialization();
}

void pysc_signal_handler(int sig) {
  if (sig == SIGINT) {
    sc_core::sc_status status = sc_core::sc_get_status();
    if (status == sc_core::SC_RUNNING) {
      sc_core::sc_pause();
    } else if(status == sc_core::SC_PAUSED) {
      cpp_sigint(sig);
    }
    return;
  }
  sc_core::sc_stop();
  wait(SC_ZERO_TIME);
  if (sig == SIGTERM) {
    cpp_sigterm(sig);
  }
}

void pysc_start() {
  python->end_of_initialization();
  cpp_sigint = python->signal(SIGINT, &pysc_signal_handler);
  cpp_sigterm = python->signal(SIGTERM, &pysc_signal_handler);
  sc_core::sc_status status = sc_core::SC_RUNNING;
  while(1) {
    if (status == sc_core::SC_RUNNING) {
      sc_core::sc_start();
    } else if (status == sc_core::SC_PAUSED) {
      python->pause_of_simulation();
    } else {
      break;
    }
    status = sc_core::sc_get_status();
  }
  python->start_of_evaluation();
  python->end_of_evaluation();
}

void pysc_start(const sc_time& duration, sc_starvation_policy p = SC_RUN_TO_TIME) {
  python->end_of_initialization();
  cpp_sigint = python->signal(SIGINT, &pysc_signal_handler);
  cpp_sigterm = python->signal(SIGTERM, &pysc_signal_handler);
  sc_core::sc_status status = sc_core::SC_RUNNING;
  while(1) {
    if (status == sc_core::SC_RUNNING) {
      sc_core::sc_start(duration, p);
    } else if (status == sc_core::SC_PAUSED) {
      python->pause_of_simulation();
    } else {
      break;
    }
    status = sc_core::sc_get_status();
  }
  python->start_of_evaluation();
  python->end_of_evaluation();
}

void pysc_start(double duration, sc_time_unit unit, sc_starvation_policy p = SC_RUN_TO_TIME) {
  python->end_of_initialization();
  cpp_sigint = python->signal(SIGINT, &pysc_signal_handler);
  cpp_sigterm = python->signal(SIGTERM, &pysc_signal_handler);
  sc_core::sc_status status = sc_core::SC_RUNNING;
  while(1) {
    if (status == sc_core::SC_RUNNING) {
      sc_core::sc_start(duration, unit, p);
    } else if (status == sc_core::SC_PAUSED) {
      python->pause_of_simulation();
    } else {
      break;
    }
    status = sc_core::sc_get_status();
  }
  python->start_of_evaluation();
  python->end_of_evaluation();
}
/// @}


