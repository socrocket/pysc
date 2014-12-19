%include "usi/sc_object.i"

%{
#include "usi.h"
#include "core/common/sc_find.h"
%}

%typedef PyObject * USIObject;

%define USI_REGISTER_MODULE(name)
%header %{
USI_REGISTER_MODULE(name);
%}
%enddef
