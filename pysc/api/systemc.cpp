// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file systemc.cpp
/// 
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author 
///
#include "pysc/api/systemc.h"
#include "pysc/module.h"

#include <map>

PyScRegisterSWIGModule(pysystemc);

namespace pysc {
namespace api {
namespace systemc {

static std::map<PyObject*, sc_core::sc_event*> event_map;
static std::map<PyObject*, const sc_core::sc_event*> event_const_map;
const sc_core::sc_event *current_event;

void set_current_event(const sc_core::sc_event *e) {
  current_event = e;
}

void event_bind(PyObject* e, PyObject* obj) {
  if (!obj) {
    // create a new event (can be notified)
    event_map[e] = new sc_core::sc_event();
  } else {
    // bind to an existing event (which is constant, cannot be notified)
    event_const_map[e] = current_event;
  }
}

bool event_notify(PyObject *e) {
  std::map<PyObject *, sc_core::sc_event *>:: iterator i = event_map.find(e);
  if(i == event_map.end()) return false;
  i->second->notify();
  return true;
}

bool event_notify(PyObject *e, double time, sc_core::sc_time_unit tu) {
  std::map<PyObject *, sc_core::sc_event *>:: iterator i = event_map.find(e);
  if(i == event_map.end()) return false;
  i->second->notify(time, tu);
  return true;
}

void event_remove(PyObject *e) {
  // called by the Python destructor of a gs.event() object
  std::map<PyObject *, sc_core::sc_event *>:: iterator i = event_map.find(e);
  if(i != event_map.end()) {
    delete i->second;
    event_map.erase(i);
  }
  std::map<PyObject *, const sc_core::sc_event *>:: iterator j = event_const_map.find(e);
  if(j != event_const_map.end()) {
    event_const_map.erase(j);
  }
}

template<class T>
T callback_to_user_py(PyObject *cb, T postproc(PyObject*,PyObject*,bool*)) {
  // Python interpreter can not track stack through C++, so all such
  // callbacks are in a new Python thread.
  PyThreadState *callback_state = PyThreadState_New(PyScThisModule());
  PyEval_AcquireThread(callback_state);
  PyObject *pResult  = PyObject_CallObject(cb, NULL);

  if (pResult == NULL) {
    if(PyErr_Occurred() != NULL) {
      PyErr_Print();
      PyEval_ReleaseThread(callback_state);
      PyThreadState_Clear(callback_state);
      PyThreadState_Delete(callback_state);
      exit(-1);
    }
    //Unlucky case if PyErr_Occurred() returned NULL
    std::cout << "ERROR: Executing a python callback. No more info, sorry."
              << std::endl;
    PyEval_ReleaseThread(callback_state);
    PyThreadState_Clear(callback_state);
    PyThreadState_Delete(callback_state);
    exit(-1);
  }
  // Successful completion of callback
  // User-supplied post-processing, which typically decrements ref count of
  // callback and converts the result to the desired type
  // postprocessing has to be done before thread-state is given up and destroyed
  bool err_hint = false;
  T rv = postproc(cb, pResult, &err_hint);
  if(err_hint && PyErr_Occurred()) {
    PyErr_Print();
    PyEval_ReleaseThread(callback_state);
    PyThreadState_Clear(callback_state);
    PyThreadState_Delete(callback_state);
    exit(-1);
  }
  Py_DECREF(pResult);
  PyEval_ReleaseThread(callback_state);
  PyThreadState_Clear(callback_state);
  PyThreadState_Delete(callback_state);
  return rv;
}

bool decref_callback(PyObject *cb, PyObject *r, bool *eh) {
  Py_DECREF(cb);
  return true;
}

void start() {
  // must be in the kernel thread on entry.  Exit it so we
  // know that no thread is active on entry to any other function
  // called by the kernel
  PyEval_ReleaseThread(PyScThisModule());
  sc_core::sc_start();
  // re-acquire thread before returning control to Python
  PyEval_AcquireThread(PyScThisModule());
}

void start(double time, sc_core::sc_time_unit tu) {
  // must be in the kernel thread on entry.  Exit it so we
  // know that no thread is active on entry to any other function
  // called by the kernel
  PyEval_ReleaseThread(PyScThisModule());
  sc_core::sc_start(sc_core::sc_time(time, tu));
  // re-acquire thread before returning control to Python
  PyEval_AcquireThread(PyScThisModule());
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
  PyEval_AcquireThread(_save);
}

#if 0
void wait(PyObject* e) {
  // relinquish thread lock and set current thread to NULL
  PyThreadState *_save = PyEval_SaveThread();
  if (event_const_map[e]) {
      sc_core::wait(*event_const_map[e]);
  } else {
      sc_core::wait(*event_map[e]);
  }
  // now re-establish the previous thread
  PyEval_AcquireThread(_save);
}
#endif

double simulation_time(sc_core::sc_time_unit tu) {
  return sc_core::sc_time_stamp().to_seconds() / sc_core::sc_time(1,tu).to_seconds();
}

double delta_count() {
  return sc_core::sc_delta_count();
}

long get_curr_process_handle() {
#if SYSTEMC_API == 210
  return (long) sc_core::sc_get_curr_process_handle();
#elif SYSTEMC_API == 220 || SYSTEMC_API == 230
  return (long) sc_core::sc_get_curr_simcontext()->get_curr_proc_info()->process_handle;
#else
#error Unknown SystemC API to call for sc_get_current_process_handle
  return 0l;
#endif
}


// Function: gsp_sc_is_running
bool is_running() {
#if SYSTEMC_API == 210
  return sc_core::sc_get_curr_simcontext()->is_running();
#elif SYSTEMC_API == 220 || SYSTEMC_API == 230
  return sc_core::sc_is_running();
#else
#error Unknown SystemC API to call for sc_is_running
  return false;
#endif
}

/*
extern void sc_core::pln();
void print_sc_splash() {
  sc_core::pln();
}*/

}; // systemc
}; // api
}; // pysc
/// @}