// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file mtrace.i
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module mtrace
%include "usi.i"

USI_REGISTER_MODULE(mtrace);

%inline %{
#include <mcheck.h>
static void start() {
  // must be in the kernel thread on entry.  Exit it so we
  // know that no thread is active on entry to any other function
  // called by the kernel
  ::mtrace();
  // re-acquire thread before returning control to Python
}

static void end() {
  // must be in the kernel thread on entry.  Exit it so we
  // know that no thread is active on entry to any other function
  // called by the kernel
  ::muntrace();
  // re-acquire thread before returning control to Python
}
%}
