#include <systemc.h>
#include "pysc.h"

int sc_main(int argc, char *argv[]) {
  PythonModule *p =new PythonModule("p", "./test1.py");
  sc_start();
  return 0;
}
