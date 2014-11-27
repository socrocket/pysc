%{
#include "usi.h"
#include "core/common/sc_find.h"
%}

%define USI_REGISTER_MODULE(name)
%header %{
USI_REGISTER_MODULE(name);
%}
%enddef
