// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file usi.i
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
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
