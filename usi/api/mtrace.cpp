// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file mtrace.cpp
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer
#include "usi.h"
#include "usi/api/mtrace.h"
#include <mcheck.h>

USI_REGISTER_MODULE(_mtrace);

namespace pysc {
namespace api {
namespace mtrace {
void mtrace_start() {
  // must be in the kernel thread on entry.  Exit it so we
  // know that no thread is active on entry to any other function
  // called by the kernel
  PyEval_ReleaseThread(PyScThisModule());
  ::mtrace();
  // re-acquire thread before returning control to Python
  PyEval_AcquireThread(PyScThisModule());
}

void mtrace_end() {
  // must be in the kernel thread on entry.  Exit it so we
  // know that no thread is active on entry to any other function
  // called by the kernel
  PyEval_ReleaseThread(PyScThisModule());
  ::muntrace();
  // re-acquire thread before returning control to Python
  PyEval_AcquireThread(PyScThisModule());
}

}; // mtrace
}; // api
}; // pysc
/// @}

