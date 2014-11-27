%module parameter_

%include "std_map.i"
%include "std_string.i"

namespace std {
   %template(mapss) map<string,string>;
};

%{
#include "usi/api/parameter.h"
%}

%include "usi/api/parameter.h"
