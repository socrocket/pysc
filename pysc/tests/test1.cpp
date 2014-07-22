// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file test1.cpp
///
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author
///
#include "pysc.h"
#include <systemc.h>

int sc_main(int argc, char *argv[]) {
  /*PythonModule *p =*/ new PythonModule("p", "./test1.py");
  sc_start();
  return 0;
}
/// @}
