%include "usi/sc_object.i"

%begin %{
#include <Python.h>
#include <cstddef>
using std::ptrdiff_t;
%}

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
