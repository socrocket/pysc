%module _report

%include "usi.i"
%include "std_string.i"

%{
USI_REGISTER_MODULE(_report);
%}

namespace sc_core {
enum sc_severity {
    SC_INFO = 0,        // informative only
    SC_WARNING, // indicates potentially incorrect condition
    SC_ERROR,   // indicates a definite problem
    SC_FATAL,   // indicates a problem from which we cannot recover
    SC_MAX_SEVERITY
};
}

void set_filter_to_whitelist(bool value);
void add_sc_object_to_filter(std::string name, sc_core::sc_severity severity, int verbosity);
void remove_sc_object_from_filter(std::string name);


%{
#include "core/common/report.h"

void set_filter_to_whitelist(bool value) {
  sr_report_handler::set_filter_to_whitelist(value);
}

void add_sc_object_to_filter(std::string name, sc_severity severity, int verbosity) {
  sc_core::sc_object *obj = sc_find_by_name(name.c_str());
  if(obj) {
    sr_report_handler::add_sc_object_to_filter(obj, severity, verbosity);
  }
}

void remove_sc_object_from_filter(std::string name) {
  sc_core::sc_object *obj = sc_find_by_name(name.c_str());
  if(obj) {
    sr_report_handler::remove_sc_object_from_filter(obj);
  }
}
%}


