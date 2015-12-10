// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file intrinsic.i
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module intrinsics

%include "std_string.i"
%include "stdint.i"
%include "usi.i"
%include "typemaps.i"

USI_REGISTER_MODULE(intrinsics)

%{
#include "core/common/sr_iss/intrinsics/intrinsicmanager.h"
#include "core/common/sr_iss/intrinsics/platformintrinsic.h"
%}

%inline %{
template<class issueWidth>
class IntrinsicInterface {
  public:
#ifndef SWIG
    IntrinsicInterface(): m_manager(NULL) {}
    IntrinsicInterface(IntrinsicManager<issueWidth> *manager): m_manager(manager) {}
#endif
    unsigned int get_exit_value() {
      return m_manager->processorInstance.getExitValue();
    }
    bool register_intrinsic(issueWidth addr, sc_core::sc_object *obj) {
      PlatformIntrinsic<issueWidth> *instance = dynamic_cast<PlatformIntrinsic<issueWidth> *>(obj);
      if(obj) {
        m_manager->register_intrinsic(addr, *instance);
        instance->setManager(m_manager);
        instance->setProcessor(&m_manager->processorInstance);
        return true;
      } else {
        // TODO(rmeyer): Error
        return false;
      }
    }
  private:
    IntrinsicManager<issueWidth> *m_manager;
};
%}
%include "core/common/sr_iss/intrinsics/platformintrinsic.h"
%template (IntrinsicInterface32) IntrinsicInterface<unsigned int>;
%template (PlatformIntrinsic32) PlatformIntrinsic<unsigned int>;
%{
typedef IntrinsicInterface<unsigned int> IntrinsicInterface32;
typedef PlatformIntrinsic<unsigned int> PlatformIntrinsic32;
#define SWIGTYPE_p_IntrinsicInterface32 SWIGTYPE_p_IntrinsicInterfaceT_unsigned_int_t
PyObject *find_usi_intrinsicmanager32(sc_core::sc_object *obj, std::string name) {
  IntrinsicManager<unsigned int> *instance = dynamic_cast<IntrinsicManager<unsigned int> *>(obj);
  if(instance) {
    return SWIG_NewPointerObj(SWIG_as_voidptr(new IntrinsicInterface32(instance)), SWIGTYPE_p_IntrinsicInterfaceT_unsigned_int_t, SWIG_POINTER_OWN | 0);
  } else {
    return NULL;
  }
}
USI_REGISTER_OBJECT_GENERATOR(find_usi_intrinsicmanager32);
#define SWIGTYPE_p_PlatformIntrinsic32 SWIGTYPE_p_PlatformIntrinsicT_unsigned_int_t
USI_REGISTER_OBJECT(PlatformIntrinsic32);
%}

