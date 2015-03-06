// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file delegate.i
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module delegate

%include "std_string.i"
%include "std_vector.i"
%include "usi.i"

USI_REGISTER_MODULE(delegate)

%extend USIDelegate {
  %pythoncode {
    def __dir__(self):
        result = set()
        for iface in self.get_if_tuple():
            result.update(dir(iface))
        result.discard('this')
        return sorted(result)

    def __getattr__(self, name):
        result = None
        for iface in self.get_if_tuple():
            result = getattr(iface, name, None)
            if result:
                return result
        super(InterfaceDelegate, self).__getattr__(name)
  }
}

%include "usi/core/delegate.h"

%{
#include "usi/core/delegate.h"

USIObject find_USIBaseDelegate(sc_core::sc_object *obj, std::string name) {
  if(obj) {
    return SWIG_NewPointerObj(SWIG_as_voidptr(new USIBaseDelegate(obj)), SWIGTYPE_p_USIBaseDelegate, SWIG_POINTER_OWN | 0);
  } else {
    return NULL;  
  }
}
USI_REGISTER_OBJECT_GENERATOR(find_USIBaseDelegate);

USIObject USIObjectFromUSIDelegate(sc_core::sc_object *obj) {
    return SWIG_NewPointerObj(SWIG_as_voidptr(new USIDelegate(obj)), SWIGTYPE_p_USIDelegate, SWIG_POINTER_OWN | 0);
}

USIDelegate USIObjectToUSIDelegate(USIObject obj) {
  USIDelegate *result = NULL;
  /// @TODO: reference counting?
  SWIG_ConvertPtr(obj, SWIG_as_voidptrptr(&result), SWIGTYPE_p_USIDelegate, 0 |  0 );
  return *result;
}

bool USIObjectIsUSIDelegate(USIObject obj) {
  USIDelegate *arg = NULL;
  return SWIG_IsOK(SWIG_ConvertPtr(obj, SWIG_as_voidptrptr(&arg), SWIGTYPE_p_USIDelegate, 0 |  0 ));
}

%}
