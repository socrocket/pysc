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
void PythonModule::report_handler(const sc_report& rep, const sc_actions& actions) {
  if( actions & (SC_DISPLAY | SC_LOG)) {
    PyObject *obj = SWIG_NewPointerObj(&rep, SWIGTYPE_p_sc_core__sc_report, 0);
    run_py_callback("report", obj)
    *log_stream << rep.get_time() << ": " << sc_report_compose_message(rep) << ::std::endl;

  }


  if(actions & SC_STOP) {
    sc_stop_here(rep.get_msg_type(), rep.get_severity());
    sc_stop();
  }

  if(actions & SC_INTERRUPT) {
    sc_interrupt_here(rep.get_msg_type(), rep.get_severity());
  }

  if(actions & SC_ABORT) {
    abort();
  }

  if(actions & SC_THROW) {
    sc_process_b* proc_p = sc_get_current_process_b();
    if(proc_p && proc_p->is_unwinding()) {
      proc_p->clear_unwinding();
    }
    throw rep; 
  }
}


%}
