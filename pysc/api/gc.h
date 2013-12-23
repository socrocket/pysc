#ifndef PYSC_API_GSPARAM_H
#define PYSC_API_GSPARAM_H

#include <Python.h>

// GreenConfig
#include "greencontrol/config.h"

namespace pysc {
namespace api {
namespace gc {

bool exists(std::string name);
std::string read(std::string name);
void write(std::string name, std::string value);

class ParamList {
    public:
        ParamList(std::string name);
        int length();
        std::string read(int i);
    private:
        std::vector<std::string> all_params;
};

ParamList list(std::string name);

/*
// functions for parameter object creation //
class Param {
public:
  // constructor for a standalone param or a param child of an extended array.
  // if a child, the parent is found in a global variable
  Param(std::string name, std::string default_val);
  // constructor for a param child of a simple array.  parent is in a global
  // makes this into a std::string.  in this case all
  // get/set go through the parent, and the default val is used if the parent
  // notes that the size from the dB is smaller than the index; in this case
  // the default val should also be applied to the dB.
  Param(unsigned index, std::string default_val);
  ~Param();

  std::string get();
  void set(std::string val);

  void set_param_as_current();

  operator gs::gs_param<std::string> *() {
      if(m_is_array_element) {
          return 0;
      } else {
          return m_param;
      }
  }
private:
  gs::gs_param<std::string> *m_param;
  gs::gs_param<std::string *> *m_parent;

  bool m_is_array_element;
  unsigned m_index_in_array;
  bool m_has_parent;
};

class ParamArray {
    // user may supply default-vector which gives actual size and default values
    // but this is dealt with in Python
    public:
        // constructor for a standalone param or a param child of an extended array.
        // if a child, the parent is found in a global variable
        ParamArray(std::string name);
        // the following constructor is for a child of a simple array and will fail
        // with the current version of GreenConfig.  parent is found in a global
        ParamArray(unsigned index);
        ~ParamArray();

        unsigned db_length();
        unsigned length();
        void length(unsigned length);


        // function to call before the construction of a child param
        void make_parent();

        operator gs::gs_param<std::string *> *() {
            return m_param;
        }
    private:
        gs::gs_param<std::string *> *m_param;
        unsigned m_length_from_db;
        bool m_has_parent;
};

class ExtParamArray {
    // user may supply a default-dict which gives actual structure and default values
    // but this is dealt with in Python
    public:
        // constructor for a standalone param or a param child of an extended array.
        // if a child, the parent is found in a global variable
        ExtParamArray(std::string name);
        // the following constructor is for a child of a simple array and will fail
        // with the current version of GreenConfig.  parent is found in a global
        ExtParamArray(unsigned index);
        virtual ~ExtParamArray();

        // function to call before the construction of a child param
        void make_parent();

        operator gs::gs_param_array *(){
            return m_param;
        }
    private:
        gs::gs_param_array *m_param;
        bool m_has_parent;
};
*/
}; // gc
}; // api
}; // pysc

#endif // PYSC_API_GSPARAM_H
