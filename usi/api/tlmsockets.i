// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file tlmsockets.i
///
/// @date 2016-
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
%module tlmsocket

%include "std_string.i"
%include "stdint.i"
%include "usi.i"

USI_REGISTER_MODULE(tlmsocket)

%begin %{
#include "tlm_utils/simple_initiator_socket.h"
#include "tlm_utils/simple_target_socket.h"
typedef tlm::tlm_initiator_socket<32, tlm::tlm_base_protocol_types, 0> iscb_320;
typedef tlm::tlm_initiator_socket<32, tlm::tlm_base_protocol_types, 1> iscb_321;
typedef tlm::tlm_target_socket<32, tlm::tlm_base_protocol_types, 0> tscb_320;
typedef tlm::tlm_target_socket<32> tscb_321;

//typedef gs::socket::bind_checker<tlm::tlm_base_protocol_types> bchk;
%}

%inline %{
class USITLMInitiatorSocket {
  public:
    USITLMInitiatorSocket(sc_core::sc_object *obj) : type(NONE), m_obj(obj) {
      if(socket<iscb_320>()) {
        type = ISCB_320;
      } else if(socket<iscb_321>()) {
        type = ISCB_321;
      }
    }
    ~USITLMInitiatorSocket() {}

    void socket_bind(sc_core::sc_object *obj) {
      switch(type) {
        case ISCB_320: {
          iscb_320::base_target_socket_type *o = dynamic_cast<iscb_320::base_target_socket_type *>(obj);
          if(o) {
            socket<iscb_320>()->bind(*o);
            return;
          } else {
            std::cout << m_obj->name() << " ISCB_320 socket given does not cast to base_target_socket_type: " << obj->name() << std::endl;
            return; /// @TODO Error
          }
        } break;
        case ISCB_321: {
          iscb_321::base_target_socket_type *o = dynamic_cast<iscb_321::base_target_socket_type *>(obj);
          if(o) {
            socket<iscb_321>()->bind(*o);
            return;
          } else {
            std::cout << m_obj->name() << " ISCB_321 socket given does not cast to base_target_socket_type " << obj->name() << std::endl;
            return; /// @TODO Error
          }
        } break;
        default: return; /// @TODO Error
      }
    }
/*
    unsigned int socket_get_num_bindings() {
      switch(type) {
        case ISCB_320: {
          return socket<iscb_320>()->size();
        } break;
        case ISCB_321: {
          return 1;
        } break;
        default: return 0; /// @TODO Error
      }
    }
    sc_core::sc_object *socket_get_other_side(uint32_t id = 0) {
      uint32_t a = 0;
      return dynamic_cast<sc_object *>(socket<bchk>()->get_other_side(id, a));
    }
*/
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

class USITLMTargetSocket {
  public:
    USITLMTargetSocket(sc_core::sc_object *obj) : type(NONE), m_obj(obj) {
      if(socket<tscb_320>()) {
        type = TSCB_320;
      } else if(socket<tscb_321>()) {
        type = TSCB_321;
      }
    }
    ~USITLMTargetSocket() {}
/*
    unsigned int socket_get_num_bindings() {
      switch(type) {
        case TSCB_320: {
          return socket<tscb_320>()->size();
        } break;
        case TSCB_321: {
          return 1;
        } break;
        default: return 0; /// @TODO Error
      }
    }
    sc_core::sc_object *socket_get_other_side(uint32_t id = 0) {
      uint32_t a = 0;
      return dynamic_cast<sc_object *>(socket<bchk>()->get_other_side(id, a));
    }
*/
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
USIObject find_USITLMInitiatorSocket_object(sc_core::sc_object *obj, std::string name) {
  PyObject *result = NULL;
  USITLMInitiatorSocket *instance = new USITLMInitiatorSocket(obj);
  if(instance) {
    if(instance->type != USITLMInitiatorSocket::NONE) {
      result = SWIG_NewPointerObj(SWIG_as_voidptr(instance), SWIGTYPE_p_USITLMInitiatorSocket, 1);
    } else {
      delete instance;
    }
  }
  return result;
}

USIObject find_USITLMTargetSocket_object(sc_core::sc_object *obj, std::string name) {
  PyObject *result = NULL;
  USITLMTargetSocket *instance = new USITLMTargetSocket(obj);
  if(instance) {
    if(instance->type != USITLMTargetSocket::NONE) {
      result = SWIG_NewPointerObj(SWIG_as_voidptr(instance), SWIGTYPE_p_USITLMTargetSocket, 1);
    } else {
      delete instance;
    }
  }
  return result;
}
USI_REGISTER_OBJECT_GENERATOR(find_USITLMInitiatorSocket_object);
USI_REGISTER_OBJECT_GENERATOR(find_USITLMTargetSocket_object);
%}

