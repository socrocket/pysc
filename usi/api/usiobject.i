// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file usiobject.i
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module usiobject

%include "std_string.i"
%include "std_vector.i"
%include "usi.i"

USI_REGISTER_MODULE(usiobject)

%pythoncode %{
class InterfaceDelegate(object):
    def __init__(self, ifs):
        self.__ifs__ = ifs
        super(InterfaceDelegate, self).__init__()

    def __dir__(self):
        result = set()
        for iface in self.__ifs__:
            result.update(dir(iface))
        result.discard('this')
        return sorted(result)

    def __getattr__(self, name):
        result = None
        for iface in self.__ifs__:
            result = getattr(iface, name, None)
            if result:
                return result
        super(InterfaceDelegate, self).__getattr__(name)
%}

%feature("pythonappend") usiobject::parent() %{
  val = find_obj(val)
%}

%feature("pythonappend") usiobject::children() %{
  val = find_obj(val)
%}

%feature("pythonappend") find(std::string) %{
  val = InterfaceDelegate(val)
%}

%feature("pythonappend") find_obj(usiobject) %{
  val = InterfaceDelegate(val)
%}


%inline %{
#include <systemc.h>
#include <vector>

class usiobject {
  public:
    const char *name() { return (m_object) ? m_object->name(): ""; }
    const char *basename() { return (m_object) ? m_object->basename(): ""; }
    const char *kind() { return (m_object) ? m_object->kind(): ""; }
    usiobject parent() {
      if(m_object) {
        return usiobject(m_object->get_parent());
      } else {
        return usiobject();
      }
    }
    std::vector<usiobject> children() {
      std::vector<usiobject> result;
      if(m_object) {
        std::vector<sc_core::sc_object *> objs = m_object->get_child_objects();
        for(std::vector<sc_core::sc_object *>::iterator iter = objs.begin(); iter != objs.end(); ++iter) {
          result.push_back(usiobject(*iter));
        }
      }
      return result;
    }
#ifndef SWIG
    usiobject(): m_object(NULL) {}
    usiobject(sc_core::sc_object *obj): m_object(obj) {}
    friend PyObject *find_obj(const usiobject &);
  private:
    sc_core::sc_object *m_object;
#endif
};

PyObject *find_obj(const usiobject &obj) {
  return PyScObjectGenerator::find_object_by_ptr(obj.m_object);
}

PyObject *find(std::string name) {
  return PyScObjectGenerator::find_object_by_name(name.c_str());
}
%}

%{
PyObject *find_usiobject(sc_core::sc_object *obj, std::string name) {
  return SWIG_NewPointerObj(SWIG_as_voidptr(new usiobject(obj)), SWIGTYPE_p_usiobject, SWIG_POINTER_OWN | 0); \
}
USI_REGISTER_OBJECT_GENERATOR(find_usiobject);
%}
namespace std {
   %template(vector_of_usiobject) vector<usiobject>;
};

