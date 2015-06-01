#ifndef USI_CORE_DELEGATE_H_
#define USI_CORE_DELEGATE_H_

#include <systemc.h>
#include <vector>
#include "usi.h"
#include "core/common/gs_config.h"

class USIDelegate;

class USIBaseDelegate {
  public:
    const char *name() {
      gs::cnf::gs_param_base *param = dynamic_cast<gs::cnf::gs_param_base *>(m_object);
      if(param) {
        return param->getName().c_str();
      } else if(m_object) {
        return m_object->name();
      } else {
        return "";
      }

    }
    const char *basename() {
      gs::cnf::gs_param_base *param = dynamic_cast<gs::cnf::gs_param_base *>(m_object);
      if(param) {
        size_t offset = 0;
        sc_core::sc_object *parent = m_object->get_parent();
        gs::cnf::gs_param_base *parent_param = dynamic_cast<gs::cnf::gs_param_base *>(parent);
        if(parent_param) {
          offset = parent_param->getName().length();
        } else if(parent) {
          offset = sizeof(parent->name());
        }
        if(offset) {
          offset++;
        }
        return param->getName().substr(offset).c_str();
      } else if(m_object) {
        return m_object->basename();
      } else {
        return "";
      }
    }
    const char *kind() {
      gs::cnf::gs_param_base *param = dynamic_cast<gs::cnf::gs_param_base *>(m_object);
      if(param) {
        return param->getTypeString().c_str();
      } else if(m_object) {
        return m_object->kind();
      } else {
        return "";
      }
    }
    size_t id() {
      return reinterpret_cast<size_t>(m_object);
    }

    sc_core::sc_object *parent() {
      if(m_object) {
        return m_object->get_parent();
      } else {
        return NULL;
      }
    }

    std::vector<sc_core::sc_object *> children() {
      if(m_object) {
        return m_object->get_child_objects();
      } else {
        return std::vector<sc_core::sc_object *>();
      }
    }

#ifndef SWIG
    USIBaseDelegate(): m_object(NULL) {}
    USIBaseDelegate(sc_core::sc_object *obj): m_object(obj) {}

  private:
    sc_core::sc_object *m_object;
#endif
};

class USIDelegate {
  public:
    USIDelegate(std::string name) {
      this->m_object = PyScObjectGenerator::find_object_by_name(name);
      this->ifs = PyScObjectGenerator::find_object_by_ptr(m_object);
      // Returns a new reference
    }

#ifndef SWIG
    USIDelegate(sc_core::sc_object *obj) : m_object(obj) {
      this->ifs = PyScObjectGenerator::find_object_by_ptr(m_object);
      // Returns a new reference
    }

    sc_core::sc_object *toObject() {
      return this->m_object;
    }

    operator sc_core::sc_object *() {
      return this->m_object;
    }
#endif

    ~USIDelegate() {
      /// @todo Decrement ifs count  
      Py_XDECREF(this->ifs);
    }

    USIObject get_if_tuple() {
      Py_XINCREF(this->ifs);
      return ifs;
    }

  private:
    USIObject ifs;
    sc_core::sc_object *m_object;
};

#ifndef SWIG
USIObject USIObjectFromUSIDelegate(sc_core::sc_object *obj);
USIDelegate *USIObjectToUSIDelegate(USIObject obj);
bool USIObjectIsUSIDelegate(USIObject obj);
#endif

#endif  // USI_CORE_DELEGATE_H_
