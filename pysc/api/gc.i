%module pygc

// Avoid warning "Nothing known about base class"
//#pragma SWIG nowarn=401

%include "std_map.i"
%include "std_string.i"

namespace std {
   %template(mapss) map<string,string>;
};

//%typemap(throws) gs::msg::invalid_receiver {
//   SWIG_exception(SWIG_RuntimeError, $1.what());
//}

%{
#include "pysc/api/gc.h"
%}

%include "pysc/api/gc.h"
