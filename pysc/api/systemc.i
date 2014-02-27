%module pysystemc

%include "std_string.i"

%{
#include "pysc/api/systemc.h"
#include <sysc/utils/sc_report.h>
%}

%include "pysc/api/systemc.h"
%include "sysc/utils/sc_report.h"

%{
#include "pysc/pysc.h"
void PythonModule::report_handler(const sc_core::sc_report &rep, const sc_core::sc_actions &actions) {
  if( actions & (sc_core::SC_DISPLAY | sc_core::SC_LOG)) {
    PyObject *obj = SWIG_NewPointerObj((void *)&rep, SWIGTYPE_p_sc_core__sc_report, 0);
    PyObject *args = Py_BuildValue("[O]", obj);
    PythonModule::globalInstance->run_py_callback("report", args);
    // *log_stream << rep.get_time() << ": " << sc_report_compose_message(rep) << ::std::endl;
    Py_DECREF(args);
    Py_DECREF(obj);
  }

  if(actions & (sc_core::SC_STOP | sc_core::SC_ABORT | sc_core::SC_INTERRUPT | sc_core::SC_THROW)) {
    sc_core::sc_report_handler::default_handler(rep, actions & ~(sc_core::SC_DISPLAY | sc_core::SC_LOG));
  }
}


%}
