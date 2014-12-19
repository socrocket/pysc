
%{
#include "usi/core/delegate.h"
%}

%typemap(typecheck) sc_core::sc_object {
  $1 = USIObjectIsUSIDelegate($input)? 1 : 0;
}

%typemap(in) sc_core::sc_object * {
  $1 = (sc_core::sc_object *)USIObjectToUSIDelegate;
}

%typemap(out) sc_core::sc_object * {
  $result = USIObjectFromUSIDelegate($1);
}

%typemap(out) std::vector<sc_core::sc_object *> {
  $result = PyList_New($1.size());
  for(size_t i = 0; i < $1.size(); ++i) {
    PyList_SetItem($result, i, USIObjectFromUSIDelegate($1.at(i)));
  }
}
