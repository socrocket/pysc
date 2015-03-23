#ifndef USI_CORE_DELEGATE_H_
#define USI_CORE_DELEGATE_H_

#include <systemc.h>
#include <vector>
#include "usi.h"

class USIDelegate;

class USIBaseDelegate {
  public:
    const char *name() { return (m_object) ? m_object->name(): ""; }
    const char *basename() { return (m_object) ? m_object->basename(): ""; }
    const char *kind() { return (m_object) ? m_object->kind(): ""; }
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
