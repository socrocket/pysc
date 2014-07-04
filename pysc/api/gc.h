// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file gc.h
/// 
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author 
///
#ifndef PYSC_API_GSPARAM_H
#define PYSC_API_GSPARAM_H

#include <Python.h>

// GreenConfig
#include <greencontrol/config.h>

#if SWIG
namespace gs {
  namespace cnf {
    enum callback_type {
      pre_read,
      post_read,
      reject_write,
      pre_write,
      post_write,
      create_param,
      destroy_param,
      post_write_and_destroy,
      no_callback
    };
  };
};
#endif

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
bool is_int(std::string name);
bool is_float(std::string name);
bool is_bool(std::string name);
bool is_array(std::string name);

void register_callback(std::string, PyObject *callback, gs::cnf::callback_type type);
void unregister_callback(PyObject *);

}; // gc
}; // api
}; // pysc

#endif // PYSC_API_GSPARAM_H
/// @}
