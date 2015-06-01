// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file registry.i
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module registry

%include "usi.i"
%include "std_string.i"
%include "std_set.i"



%{
USI_REGISTER_MODULE(registry);
%}

namespace std {
   %template(set_string) set<std::string>;
}

sc_core::sc_object *create_object_by_name(std::string group, std::string type, std::string name);
std::set<std::string> get_module_files(std::string group);

%{
#include "core/common/sr_registry.h"

sc_core::sc_object *create_object_by_name(std::string group, std::string type, std::string name) {
  return SrModuleRegistry::create_object_by_name(group, type, name);
}

std::set<std::string> get_module_files(std::string group) {
  return SrModuleRegistry::get_module_files(group);
}
%}


