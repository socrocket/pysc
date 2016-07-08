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

%pythonappend USIDelegate::USIDelegate %{
  from usi.sc_object import usi_extend_delegate
  usi_extend_delegate(self)
%}

%extend USIDelegate {
  %pythoncode {
    def __repr__(self):
        if hasattr(self, 'name'):
            return "USIDelegate('%s')" % (self.name())
        else:
            return "USIDelegate('unknown')"
            

    def __dir__(self):
        result = set(self.__dict__['if_data'].keys())
        for iface in self.__usi_interfaces__():
            result.update(dir(iface))
            if hasattr(iface, 'children') and callable(getattr(iface, 'children')):
                result.update([child.basename() for child in getattr(iface, 'children')() if hasattr(child, 'basename') and callable(getattr(child, 'basename'))])
        result.discard('this')
        return sorted(result)

    def __getattr__(self, name):
        result = self.__dict__.setdefault('if_data', {}).get(name)
        if result:
            return result
        for iface in self.__usi_interfaces__():
            result = getattr(iface, name, None)
            if result:
                return result
            if hasattr(iface, 'children') and callable(getattr(iface, 'children')):
                for child in getattr(iface, 'children')():
                    if hasattr(child, 'name') and callable(getattr(child, 'basename')) and child.basename() == name:
                        return child
                
        if hasattr(super(USIDelegate, self), name):
            super(USIDelegate, self).__getattr__(name)

    def __getitem__(self, index):
        return self.__getattr__(str(index))

    def __setattr__(self, name, value):
        if name in ["this", "if_data"]:
            self.__dict__[name] = value
        else:
            self.__dict__.setdefault('if_data', {})[name] = value
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

USIDelegate *USIObjectToUSIDelegate(USIObject obj) {
  void *argp1 = NULL;
  USIDelegate *result = NULL;
  /// @TODO: reference counting?
  if(SWIG_IsOK(SWIG_ConvertPtr(obj, &argp1, SWIGTYPE_p_USIDelegate, 0 |  0 ))) {
    result = reinterpret_cast<USIDelegate *>(argp1);
    return result;
  } else {
    return NULL;
  }
}

bool USIObjectIsUSIDelegate(USIObject obj) {
  void *arg = NULL;
  return SWIG_IsOK(SWIG_ConvertPtr(obj, &arg, SWIGTYPE_p_USIDelegate, 0 |  0 ));
}

%}
