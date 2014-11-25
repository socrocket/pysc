// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file report.cpp
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer
#include "usi.h"
#include "usi/api/report.h"
#include "core/common/report.h"
#include "core/common/sc_find.h"

USI_REGISTER_MODULE(_report);

namespace pysc {
namespace api {
namespace report {
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

}; // report
}; // api
}; // pysc
/// @}

