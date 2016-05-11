
%{
#include "usi/core/delegate.h"
%}

%typemap(typecheck) sc_object * {
  $1 = USIObjectIsUSIDelegate($input)? 1 : 0;
}

%typemap(in) sc_object * (USIDelegate *tmp) {
  tmp = USIObjectToUSIDelegate($input);
  $1 = tmp? tmp->toObject() : NULL;
}

%typemap(out) sc_object * {
  $result = USIObjectFromUSIDelegate($1);
}

%typemap(out) std::vector<sc_object *> {
  $result = PyList_New($1.size());
  for(size_t i = 0; i < $1.size(); ++i) {
    PyList_SetItem($result, i, USIObjectFromUSIDelegate($1.at(i)));
  }
}

%typemap(typecheck) sc_core::sc_object * {
  $1 = USIObjectIsUSIDelegate($input)? 1 : 0;
}

%typemap(in) sc_core::sc_object * (USIDelegate *tmp) {
  tmp = USIObjectToUSIDelegate($input);
  $1 = tmp? tmp->toObject() : NULL;
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
