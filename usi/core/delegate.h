#ifndef USI_CORE_DELEGATE_H_
#define USI_CORE_DELEGATE_H_

#include <systemc.h>
#include <vector>
#include <cstring>
#include "usi.h"
#ifndef NC_SYSTEMC
#include "core/common/sr_param.h"
#endif

/// Forward declaration of USIDelegate
/// It will be the collector object delegating the function calls to all the interfaces
class USIDelegate;

/// Base delegate implements the core sc_object functionality
/// This allows every interface to use sc_object like a primitive
class USIBaseDelegate {
  public:

    /// Returns the full name of the corresponding sc_object or gs_param
    const char *name() {
#ifndef NC_SYSTEMC
      gs::cnf::gs_param_base *param = dynamic_cast<gs::cnf::gs_param_base *>(m_object);
      if(param) {
        return param->getName().c_str();
      } else
#endif
        if(m_object) {
        return m_object->name();
      } else {
        return "";
      }

    }

    /// Returns the name of the corresponding sc_object or gs_param
    const char *basename() {
#ifndef NC_SYSTEMC
      gs::cnf::gs_param_base *param = dynamic_cast<gs::cnf::gs_param_base *>(m_object);
      if(param) {
        std::string name = param->getName();
        size_t offset = name.rfind('.') + 1;
        return name.substr(offset).c_str();
      } else
#endif
        if(m_object) {
        return m_object->basename();
      } else {
        return "";
      }
    }

    /// Returns the kind of an sc_object
    const char *kind() {
#ifndef NC_SYSTEMC
      gs::cnf::gs_param_base *param = dynamic_cast<gs::cnf::gs_param_base *>(m_object);
      if(param) {
        return param->getTypeString().c_str();
      } else
#endif
        if(m_object) {
        return m_object->kind();
      } else {
        return "";
      }
    }

    size_t id() {
      return reinterpret_cast<size_t>(m_object);
    }

    /// Returns the hierachial parent of the sc_object
    sc_core::sc_object *parent() {
      if(m_object) {
        return m_object->get_parent_object();
      } else {
        return NULL;
      }
    }

    /// Returns a list of children of the sc_object
    std::vector<sc_core::sc_object *> children() {
#ifndef NC_SYSTEMC
      gs::cnf::gs_param_array *param = dynamic_cast<gs::cnf::gs_param_array *>(m_object);
      if(param) {
        std::vector<sc_core::sc_object *> result;
        for(gs::cnf::gs_param_array::iterator iter = param->begin(); iter != param->end(); ++iter) {
          result.push_back(*iter);
        }
        return result;
      } else
#endif
      if(m_object) {
        return m_object->get_child_objects();
      } else {
        return std::vector<sc_core::sc_object *>();
      }
    }

#ifndef SWIG
    /// Default constructor because SWIG needs it
    /// Please never use! It will not be bound to any sc_object and therefore worthless
    USIBaseDelegate(): m_object(NULL) {}

    /// Constructor.
    /// The constructor takes an sc_object as parameter.
    /// It will bind to the sc_object.
    /// @param obj sc_object to bind to.
    USIBaseDelegate(sc_core::sc_object *obj): m_object(obj) {}

  private:
    /// Pointer to the corresponding sc_object
    sc_core::sc_object *m_object;
#endif
};

/// Delegation object.
/// This object handles the delegation to the different interface like USIBaseDelegator.
/// The USIBaseDelegator implements the core functionality of the sc_object interface.
/// The second half of the object is implemented in the script language dependend delegate.i
/// All we cover here in C++ is the construction and collection of interface classes.
class USIDelegate {
  public:
    /// Constructor avaliable from the scripting language.
    /// Just provide a hierachial sc_object or gs_param name and it will create a corresponding USIDelegate.
    /// @param name Hierachail name of the corresponding sc_object.
    USIDelegate(std::string name) {
      this->m_object = PyScObjectGenerator::find_object_by_name(name);
      this->m_interfaces = PyScObjectGenerator::find_object_by_ptr(m_object);
      // Returns a new reference
    }

#ifndef SWIG
    /// Copy constructor from sc_objects.
    /// Only available for convinience and only usable from C++
    /// @param obj sc_object to bind to.
    USIDelegate(sc_core::sc_object *obj) : m_object(obj) {
      this->m_interfaces = PyScObjectGenerator::find_object_by_ptr(m_object);
      // Returns a new reference
    }

    /// Return the connected sc_object.
    /// Only available in C++ and used for converting back.
    sc_core::sc_object *toObject() {
      return this->m_object;
    }

    /// conversion operator to sc_object.
    /// Only available in C++ to use for implecit convertion in other interface implementations.
    operator sc_core::sc_object *() {
      return this->m_object;
    }
#endif

    /// Destructor.
    /// Decrements the ref count of the interface implementation list.
    /// This is scripting language dependend.
    ~USIDelegate() {
      /// @todo Decrement m_interfaces count
      Py_XDECREF(this->m_interfaces);
    }

    /// Return the list of interface implementations.
    USIObject __usi_interfaces__() {
      Py_XINCREF(this->m_interfaces);
      return m_interfaces;
    }

  private:
    /// The list of collected interface implementatiion classes
    USIObject m_interfaces;

    /// The corresponding sc_object.
    sc_core::sc_object *m_object;
};

#ifndef SWIG
/// Convertion functions to translate from sc_object to an language specific object.
USIObject USIObjectFromUSIDelegate(sc_core::sc_object *obj);

/// Convertion functions to translate from an language specific object to sc_object.
USIDelegate *USIObjectToUSIDelegate(USIObject obj);

/// A function to test if a language specific object contains a USIDelegate.
bool USIObjectIsUSIDelegate(USIObject obj);
#endif

#endif  // USI_CORE_DELEGATE_H_
