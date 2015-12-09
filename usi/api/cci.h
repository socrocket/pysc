// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file cci.h
///
/// @date 2013-2015
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
#ifndef PYSC_API_CCI_H_
#define PYSC_API_CCI_H_

#include <Python.h>

// GreenConfig
#include "core/common/sr_param.h"

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
namespace cci {

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

std::string get_documentation(std::string name);
std::string get_type_string(std::string name);
PyObject *get_properties(std::string name);
void register_callback(std::string, PyObject *callback, gs::cnf::callback_type type);
void unregister_callback(PyObject *);

class USICCIParam {
  public:
    USICCIParam(gs::gs_param_base *obj) : m_object(obj) {}

    bool cci_isInteger() {
        gs::cnf::Param_type t = m_object->getType();
        return (
            (t == gs::cnf::PARTYPE_INT) ||
            (t == gs::cnf::PARTYPE_UINT) ||
            (t == gs::cnf::PARTYPE_ULONGLONG) ||
            (t == gs::cnf::PARTYPE_LONGLONG) ||
            (t == gs::cnf::PARTYPE_UCHAR) ||
            (t == gs::cnf::PARTYPE_USHORT) ||
            (t == gs::cnf::PARTYPE_SHORT) ||
            (t == gs::cnf::PARTYPE_CHAR) ||
            (t == gs::cnf::PARTYPE_SIGNED_CHAR) ||
            (t == gs::cnf::PARTYPE_SC_INT_BASE) ||
            (t == gs::cnf::PARTYPE_SC_INT) ||
            (t == gs::cnf::PARTYPE_SC_UINT_BASE) ||
            (t == gs::cnf::PARTYPE_SC_UINT) ||
            (t == gs::cnf::PARTYPE_SC_SIGNED) ||
            (t == gs::cnf::PARTYPE_SC_UNSIGNED) ||
            (t == gs::cnf::PARTYPE_SC_BIGINT) ||
            (t == gs::cnf::PARTYPE_SC_BIGUINT)
        );

    }

    bool cci_isFloat() {
        gs::cnf::Param_type t = m_object->getType();
        return (
            (t == gs::cnf::PARTYPE_FLOAT) ||
            (t == gs::cnf::PARTYPE_DOUBLE)
        );
    }

    bool cci_isBoolean() {
        gs::cnf::Param_type t = m_object->getType();
        return (
            (t == gs::cnf::PARTYPE_BOOL) ||
            (t == gs::cnf::PARTYPE_SC_LOGIC)
        );
    }

    bool cci_isArray() {
        gs::cnf::Param_type t = m_object->getType();
        return (
            (t == gs::cnf::PARTYPE_SMPL_ARRAY) ||
            (t == gs::cnf::PARTYPE_EXT_ARRAY)
        );
    }


    std::string cci_read() {
        std::string value;
        m_object->getValue(value);
        return value;
    }

    void cci_write(std::string value) {
        m_object->setString(value);
    }

    std::string cci_documentation() {
        return m_object->get_documentation();
    }

    std::string cci_typename() {
        return m_object->getTypeString();
    }

    std::string cci_name() {
        return m_object->getName();
    }

    USIObject cci_properties() {
        PyObject *dict = PyDict_New();
        sr_param_base *param = dynamic_cast<sr_param_base *>(m_object);
        if(param) {
            std::map<std::string, std::string> properties = param->getProperties();
            for(std::map<std::string, std::string>::iterator iter = properties.begin(); iter!=properties.end(); ++iter) {
                PyObject *key = PyUnicode_DecodeUTF8(iter->first.c_str(), iter->first.length(), NULL);
                PyObject *val = PyUnicode_DecodeUTF8(iter->second.c_str(), iter->second.length(), NULL);
                PyDict_SetItem(dict, key, val);
            }
        }
        return dict;
    }

    void cci_register_callback(PyObject *callback, gs::cnf::callback_type type);
    void cci_unregister_callback(PyObject *callback);

  private:
    gs::gs_param_base *m_object;
};

}  // namespace cci
}  // namespace api
}  // namesapce pysc

#endif  // PYSC_API_CCI_H
/// @}
