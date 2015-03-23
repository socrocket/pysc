// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file greensocket.i
/// 
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module greensocket

%include "std_string.i"
%include "stdint.i"
%include "usi.i"

USI_REGISTER_MODULE(greensocket)

%begin %{
#include "core/common/amba.h"
typedef gs::socket::initiator_socket_callback_base<32, tlm::tlm_base_protocol_types, 0> iscb_320;
typedef gs::socket::initiator_socket_callback_base<32, tlm::tlm_base_protocol_types, 1> iscb_321;
typedef gs::socket::target_socket_callback_base<32, tlm::tlm_base_protocol_types, 0> tscb_320;
typedef gs::socket::target_socket_callback_base<32, tlm::tlm_base_protocol_types, 1> tscb_321;
%}

%inline %{
class USISocket {
  public:
    USISocket(sc_core::sc_object *obj) : type(NONE), m_obj(obj) {
      if(socket<iscb_320>()) {
        type = ISCB_320;
      } else if(socket<iscb_321>()) {
        type = ISCB_321;
      } else if(socket<tscb_320>()) {
        type = TSCB_320;
      } else if(socket<tscb_321>()) {
        type = TSCB_321;
      }
    }

    void bind(sc_core::sc_object *obj) {
      switch(type) {
        case ISCB_320: {
          iscb_320::base_type *o = dynamic_cast<iscb_320::base_type *>(obj);
          if(o) {
            socket<iscb_320>()->bind(*o);
            return;
          } else {
            std::cout << m_obj->name() << "ISCB_320 socket given does not cast to base_type" << std::endl;
            return; /// @TODO Error
          }
        } break;
        case ISCB_321: {
          iscb_321::base_type *o = dynamic_cast<iscb_321::base_type *>(obj);
          if(o) {
            socket<iscb_321>()->bind(*o);
            return;
          } else {
            std::cout << m_obj->name() << "ISCB_321 socket given does not cast to base_type" << std::endl;
            return; /// @TODO Error
          }
        } break;
        case TSCB_320: {
          tscb_320::base_type *o = dynamic_cast<tscb_320::base_type *>(obj);
          if(o) {
            socket<tscb_320>()->bind(*o);
            return;
          } else {
            std::cout << m_obj->name() << "TSCB_320 socket given does not cast to base_type" << std::endl;
            return; /// @TODO Error
          }
        } break;
        case TSCB_321: {
          tscb_321::base_type *o = dynamic_cast<tscb_321::base_type *>(obj);
          if(o) {
            socket<tscb_321>()->bind(*o);
            return;
          } else {
            std::cout << m_obj->name() << "TSCB_321 socket given does not cast to base_type" << std::endl;
            return; /// @TODO Error
          }
        } break;
        default: return; /// @TODO Error
      }
    }

#ifndef SWIG
    enum type_t {
      NONE,
      ISCB_320,
      ISCB_321,
      TSCB_320,
      TSCB_321
    };
    type_t type;
  private:
    sc_core::sc_object *m_obj;

    template<typename T> T *socket() {
      return dynamic_cast<T *>(m_obj);
    }  
#endif
};
%}
%{
USIObject find_USISocket_object(sc_core::sc_object *obj, std::string name) {
  PyObject *result = NULL;
  USISocket *instance = new USISocket(obj);
  if(instance) {
    if(instance->type != USISocket::NONE) {
      result = SWIG_NewPointerObj(SWIG_as_voidptr(instance), SWIGTYPE_p_USISocket, 1);
    } else {
      delete instance;
    }
  }
  return result;
}
USI_REGISTER_OBJECT_GENERATOR(find_USISocket_object);
%}

