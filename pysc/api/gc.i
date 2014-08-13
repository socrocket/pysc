%module pygc

%include "std_map.i"
%include "std_string.i"

namespace std {
   %template(mapss) map<string,string>;
};

%{
#include "pysc/api/gc.h"
%}

%include "pysc/api/gc.h"
