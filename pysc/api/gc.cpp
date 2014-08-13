// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file gc.cpp
/// 
///
/// @date 2013-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author 
///
#include <map>
#include "pysc/pysc.h"
#include "pysc/api/gc.h"
#include "pysc/api/systemc.h"
#include "pysc/module.h"
#include <Python.h>

PyScRegisterSWIGModule(pygc);

namespace pysc {
namespace api {
namespace gc {

bool exists(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    return configAPI->existsParam(name);
}

std::string read(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    return configAPI->getValue(name);
}

void write(std::string name, std::string value) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    configAPI->setInitValue(name, value);
}

ParamList list(std::string name) {
    return ParamList(name);
}

ParamList::ParamList(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    all_params = configAPI->getParamList(name);
}

int ParamList::length() {
    return all_params.size();
}

std::string ParamList::read(int i) {
    return all_params[i];
}

bool is_int(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    if(configAPI) {
        gs::gs_param_base *param = configAPI->getPar(name);
        if(param) {
            gs::cnf::Param_type t = param->getType();
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
    }
    return false;
}

bool is_float(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    if(configAPI) {
        gs::gs_param_base *param = configAPI->getPar(name);
        if(param) {
            gs::cnf::Param_type t = param->getType();
            return (
                (t == gs::cnf::PARTYPE_FLOAT) ||
                (t == gs::cnf::PARTYPE_DOUBLE)
            );
        }
    }
    return false;
}

bool is_bool(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    if(configAPI) {
        gs::gs_param_base *param = configAPI->getPar(name);
        if(param) {
            gs::cnf::Param_type t = param->getType();
            return (
                (t == gs::cnf::PARTYPE_BOOL) ||
                (t == gs::cnf::PARTYPE_SC_LOGIC)
            );
        }
    }
    return false;
}

bool is_array(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    if(configAPI) {
        gs::gs_param_base *param = configAPI->getPar(name);
        if(param) {
            gs::cnf::Param_type t = param->getType();
            return (
                (t == gs::cnf::PARTYPE_SMPL_ARRAY) ||
                (t == gs::cnf::PARTYPE_EXT_ARRAY)
            );
        }
    }
    return false;
}

std::string get_documentation(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    if(configAPI) {
        gs::gs_param_base *param = configAPI->getPar(name);
        if(param) {
            return param->get_documentation();
        }
    }
    return std::string();
}

std::string get_type_string(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    if(configAPI) {
        gs::cnf::gs_param_base *param = configAPI->getPar(name);
        if(param) {
            return param->getTypeString();
        }
    }
    return std::string();
}

PyObject *get_properties(std::string name) {
  gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
  PyObject * dict = PyDict_New();
  if(configAPI) {
    gs::gs_param_base *base = configAPI->getPar(name);
    if(base) {
      gs::cnf::gs_config_base *param = dynamic_cast<gs::cnf::gs_config_base *>(base);
      if(param) {
        std::map<std::string, std::string> properties = param->getProperties();
        for(std::map<std::string, std::string>::iterator iter = properties.begin(); iter!=properties.end(); ++iter) {
          PyObject *key = PyString_FromStringAndSize(iter->first.c_str(), iter->first.length());
          PyObject *val = PyString_FromStringAndSize(iter->second.c_str(), iter->second.length());
          PyDict_SetItem(dict, key, val);
        }
        return dict;
      }
    }
  }
  return dict;
}

class CallbackAdapter : public gs::cnf::ParamCallbAdapt_b {
    public:
        CallbackAdapter(PyObject *call, void *_observer_ptr, gs::gs_param_base *_caller_param)
        : gs::cnf::ParamCallbAdapt_b(_observer_ptr, _caller_param) {
            if(!PyCallable_Check(call)) {
                PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            }
            this->callback = call;
            Py_XINCREF(callback);

        }

        ~CallbackAdapter() {
            Py_XDECREF(callback);
        }

        gs::cnf::callback_return_type call(gs::gs_param_base& param, gs::cnf::callback_type& reason) {
          PyObject *args = PyTuple_New(4);
          PyTuple_SetItem(args, 0, PyString_FromString(param.getName().c_str()));
          PyTuple_SetItem(args, 1, PyString_FromString(param.getString().c_str()));
          PyTuple_SetItem(args, 2, PyFloat_FromDouble(pysc::api::systemc::simulation_time(sc_core::SC_NS)));
          PyTuple_SetItem(args, 3, PyInt_FromLong(reason));
          PythonModule::block_threads();
          PyObject *result = PyObject_Call(callback, args, NULL);
          PythonModule::unblock_threads();

          Py_DECREF(args);
          Py_DECREF(result);
          return gs::cnf::return_nothing;
        }

    private:
        PyObject *callback;
};

std::map<PyObject *, boost::shared_ptr<gs::cnf::ParamCallbAdapt_b> > callback_map;

void register_callback(std::string name, PyObject *callback, gs::cnf::callback_type type) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    gs::gs_param_base *param = configAPI->getPar(name);
    callback_map.insert(
        std::pair<PyObject *, boost::shared_ptr<gs::cnf::ParamCallbAdapt_b> >(
            callback,
            param->registerParamCallback(
                boost::shared_ptr<gs::cnf::ParamCallbAdapt_b>(
                    new CallbackAdapter(callback, NULL, param)
                ),
                type
            )
        )
    );
}

void unregister_callback(PyObject *callback) {
    std::map<PyObject *, boost::shared_ptr<gs::cnf::ParamCallbAdapt_b> >::iterator iter =
        callback_map.find(callback);
    if(iter!=callback_map.end()) {
        iter->second->unregister_at_parameter();
        //gs::gs_param_base *param = iter->second->get_caller_param();
        //gs::cnf::ParamCallbAdapt_b *adapt = &(*iter->second);
        //param->unregisterParamCallback(adapt);
        callback_map.erase(iter);
    }
}

}; // gc
}; // api
}; // pysc
/// @}
