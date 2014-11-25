// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file report.h
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer
#ifndef PYSC_API_REPORT_H
#define PYSC_API_REPORT_H

#include <string>
#include "core/common/systemc.h"

#ifdef SWIG
namespace sc_core {
enum sc_severity {
    SC_INFO = 0,        // informative only
    SC_WARNING, // indicates potentially incorrect condition
    SC_ERROR,   // indicates a definite problem
    SC_FATAL,   // indicates a problem from which we cannot recover
    SC_MAX_SEVERITY
};
}
#endif

namespace pysc {
namespace api {
namespace report {

void set_filter_to_whitelist(bool value);
void add_sc_object_to_filter(std::string name, sc_core::sc_severity severity, int verbosity);
void remove_sc_object_from_filter(std::string name);

};
};
}; // pysc

#endif // PYSC_API_MTRACE_H
/// @}

