%module scireg

%include "usi.i"
%include "typemaps.i"
%include "std_string.i"
%include "std_vector.i"
%include "stdint.i"
%include "cstring.i"

USI_REGISTER_MODULE(scireg)

%typemap(in) sc_dt::uint64 {
  $1 = sc_dt::uint64(PyInt_AsLong($input));
}

%typemap(typecheck) sc_dt::uint64 {
  $1 = PyInt_Check($input)? 1 : 0;
}

%typemap(out) sc_dt::uint64 {
  $result = PyInt_FromLong(uint64_t($1));
}

%typemap(in) (const scireg_ns::vector_byte &v, sc_dt::uint64 size) {
  if(!PyString_Check($input)) {
    PyErr_SetString(PyExc_ValueError, "Expecting a String");
    return NULL;
  }
  $2 = sc_dt::uint64((uint64_t)PyString_Size($input));
  if(!$1) {
    $1 = new scireg_ns::vector_byte();
  }
  $1->resize(uint64_t($2));
  memcpy(&$1->at(0), PyString_AsString($input), uint64_t($2));
}

%typemap(argout) (scireg_ns::vector_byte &v, sc_dt::uint64 size) {
  if($1) {
    delete $1;
  }
}

%typemap(typecheck) (const scireg_ns::vector_byte &v, sc_dt::uint64 size) {
  $1 = PyString_Check($input)? 1 : 0;
}

%typemap(in) (scireg_ns::vector_byte &v, sc_dt::uint64 size) {
  if (!PyInt_Check($input)) {
    PyErr_SetString(PyExc_ValueError, "Expecting an integer");
    return NULL;
  }
  $2 = sc_dt::uint64(uint64(PyInt_AsLong($input)));
  if ($2 < 0) {
    PyErr_SetString(PyExc_ValueError, "Positive integer expected");
    return NULL;
  }
  if(!$1) {
    $1 = new scireg_ns::vector_byte();
  }
  $1->resize($2);
}

%typemap(typecheck) (scireg_ns::vector_byte &v, sc_dt::uint64 size) {
  $1 = PyInt_Check($input)? 1 : 0;
}

%typemap(argout) (scireg_ns::vector_byte &v, sc_dt::uint64 size) {
   Py_XDECREF($result);   /* Blow away any previous result */
   if ($result < 0) {     /* Check for I/O error */
       PyErr_SetFromErrno(PyExc_IOError);
       return NULL;
   }
   $result = PyString_FromStringAndSize(reinterpret_cast<char *>(&$1->at(0)),uint64_t($2));
   delete $1;
}

%typemap(in, numinputs=0) const char *&s (const char *null_str = "") {
  $1 = ($1_ltype)&null_str;
}

%typemap(argout) const char *&s {
   Py_XDECREF($result);   /* Blow away any previous result */
   $result = PyString_FromString(*$1);
}

%{
#include "core/common/scireg.h"
#include <map>
class usi_scireg_parent;
%}

%include "core/common/scireg.h"

void scireg_initialize();

%inline %{
class usi_scireg_parent {
  public:
    const std::vector<scireg_ns::scireg_region_if *> &sci_regions() const {
      return m_regions;
    }
#ifndef SWIG
    usi_scireg_parent() {}
    void add_region(scireg_ns::scireg_region_if *region) {
      m_regions.push_back(region);
    }
    void remove_region(scireg_ns::scireg_region_if *region) {
      for (std::vector<scireg_ns::scireg_region_if *>::iterator iter = m_regions.begin(); iter != m_regions.end(); ++iter) {
        if (*iter == region) {
          m_regions.erase(iter);
          break;
        }
      }
    }
  private:
    std::vector<scireg_ns::scireg_region_if *> m_regions;
#endif
};
%}

%{
class usi_scireg_registry : public scireg_ns::scireg_notification_if {
  public:
    usi_scireg_registry() {
      scireg_ns::scireg_tool_registry::add_tool(*this);
    }
    virtual ~usi_scireg_registry() {
      scireg_ns::scireg_tool_registry::remove_tool(*this);
    }

    virtual void add_region(scireg_ns::scireg_region_if &region) {
      m_regions.push_back(&region);
    };
    
    virtual void remove_region(scireg_ns::scireg_region_if &region) {
      std::vector<sc_core::sc_module *> parents;
      region.scireg_get_parent_modules(parents);
      for(std::vector<sc_core::sc_module *>::iterator iter = parents.begin(); iter != parents.end(); ++iter) {
        sc_core::sc_object *obj = *iter;
        usi_scireg_parent &parent = m_regionmap[obj];
        parent.remove_region(&region);
      }
    };

    usi_scireg_parent *find(sc_core::sc_object *obj) {
      std::map<sc_core::sc_object *, usi_scireg_parent>::iterator iter = m_regionmap.find(obj);
      if(iter != m_regionmap.end()) {
        return &iter->second;
      } else {
        return NULL;
      }
    }

    void initialize() {
      for(std::vector<scireg_ns::scireg_region_if *>::iterator iter = m_regions.begin(); iter != m_regions.end(); ++iter) {
        std::vector<sc_core::sc_module *> parents;
        
        if((*iter)->scireg_get_parent_modules(parents)==scireg_ns::SCIREG_SUCCESS) {
          for(std::vector<sc_core::sc_module *>::iterator iter2 = parents.begin(); iter2 != parents.end(); ++iter2) {
            sc_core::sc_object *obj = *iter2;
            usi_scireg_parent &parent = m_regionmap[obj];
            parent.add_region(*iter);
          }
        }
      }
    }

    static usi_scireg_registry *singleton;

  private:
    std::map<sc_core::sc_object *, usi_scireg_parent> m_regionmap;
    std::vector<scireg_ns::scireg_region_if *> m_regions;
};

usi_scireg_registry *usi_scireg_registry::singleton;

void scireg_initialize() {
  usi_scireg_registry::singleton->initialize();  
}

%}

%pythoncode {
  import usi
  def scireg_end_of_initialization(*k, **kw):
      scireg_initialize()

  usi.on('end_of_initialization')(scireg_end_of_initialization)
}

namespace std {
   //%template(vector_byte) vector<unsigned char>;
   %template(vector_notification_if) vector<scireg_ns::scireg_notification_if *>;
   %template(vector_region_if) vector<scireg_ns::scireg_region_if *>;
   %template(vector_mapped_region_if) vector<scireg_ns::scireg_mapped_region>;
   %template(vector_sc_object) vector<sc_core::sc_object *>;
   %template(vector_sc_module) vector<sc_core::sc_module *>;
   %template(vector_value_info) vector<scireg_ns::scireg_value_info>;
};

%{
PyObject *find_usi_scireg_parent(sc_core::sc_object *obj, std::string name) {
  usi_scireg_parent *instance = usi_scireg_registry::singleton->find(obj);
  if(instance) {
    return SWIG_NewPointerObj(SWIG_as_voidptr(instance), SWIGTYPE_p_usi_scireg_parent, 0);
  } else {
    return NULL;
  }
}
USI_REGISTER_OBJECT_GENERATOR(find_usi_scireg_parent);

PyObject *find_scireg_region_if(sc_core::sc_object *obj, std::string name) {
  scireg_ns::scireg_region_if *instance = dynamic_cast<scireg_ns::scireg_region_if *>(obj);
  if(instance) {
    return SWIG_NewPointerObj(SWIG_as_voidptr(instance), SWIGTYPE_p_scireg_ns__scireg_region_if, 0);
  } else {
    return NULL;
  }
}
USI_REGISTER_OBJECT_GENERATOR(find_scireg_region_if);
%}

%init %{
  usi_scireg_registry::singleton = new usi_scireg_registry();
%}
