%module parameter_

%include "usi.i"
%include "std_map.i"
%include "std_string.i"

namespace std {
   %template(mapss) map<string,string>;
};

%{
#include "usi/api/parameter.h"

USIObject find_cci_parameter(sc_core::sc_object *obj, std::string name) {
  gs::gs_param_base *instance = dynamic_cast<gs::gs_param_base *>(obj);
  if(instance) {
    pysc::api::gc::USICCIParam *param = new pysc::api::gc::USICCIParam(instance);
    return SWIG_NewPointerObj(SWIG_as_voidptr(param), SWIGTYPE_p_pysc__api__gc__USICCIParam, 0);
  } else {
    return NULL;
  }
}
USI_REGISTER_OBJECT_GENERATOR(find_cci_parameter);
%}

%include "usi/api/parameter.h"
