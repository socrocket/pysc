%module pygc

// Avoid warning "Nothing known about base class"
//#pragma SWIG nowarn=401

%include "std_string.i"
//%include "exception.i"

//namespace std {
//   %template(pairbi) pair<bool,int>;
//};

//%typemap(throws) gs::msg::invalid_receiver {
//   SWIG_exception(SWIG_RuntimeError, $1.what());
//}

%{
#include "pysc/api/gc.h"
%}

%include "pysc/api/gc.h"
