#include "pysc/api/gc.h"
#include "pysc/api/systemc.h"
#include "pysc/module.h"
#include <map>

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
    gs::gs_param_base *param = configAPI->getPar(name);
    gs::cnf::Param_type t = param->getType();
    return (
      (t & gs::cnf::PARTYPE_INT) |
      (t & gs::cnf::PARTYPE_UINT) |
      (t & gs::cnf::PARTYPE_ULONGLONG) |
      (t & gs::cnf::PARTYPE_LONGLONG) |
      (t & gs::cnf::PARTYPE_UCHAR) |
      (t & gs::cnf::PARTYPE_USHORT) |
      (t & gs::cnf::PARTYPE_SHORT) |
      (t & gs::cnf::PARTYPE_CHAR) |
      (t & gs::cnf::PARTYPE_SIGNED_CHAR) |
      (t & gs::cnf::PARTYPE_SC_INT_BASE) |
      (t & gs::cnf::PARTYPE_SC_INT) |
      (t & gs::cnf::PARTYPE_SC_UINT_BASE) |
      (t & gs::cnf::PARTYPE_SC_UINT) |
      (t & gs::cnf::PARTYPE_SC_SIGNED) |
      (t & gs::cnf::PARTYPE_SC_UNSIGNED) |
      (t & gs::cnf::PARTYPE_SC_BIGINT) |
      (t & gs::cnf::PARTYPE_SC_BIGUINT)
    );
}

bool is_float(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    gs::gs_param_base *param = configAPI->getPar(name);
    gs::cnf::Param_type t = param->getType();
    return (
      (t & gs::cnf::PARTYPE_FLOAT) |
      (t & gs::cnf::PARTYPE_DOUBLE)
    );
}

bool is_bool(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    gs::gs_param_base *param = configAPI->getPar(name);
    gs::cnf::Param_type t = param->getType();
    return (
      (t & gs::cnf::PARTYPE_BOOL) |
      (t & gs::cnf::PARTYPE_SC_LOGIC)
    );
}

bool is_array(std::string name) {
    gs::cnf::cnf_api *configAPI = gs::cnf::GCnf_Api::getApiInstance(NULL);
    gs::gs_param_base *param = configAPI->getPar(name);
    gs::cnf::Param_type t = param->getType();
    return (
      (t & gs::cnf::PARTYPE_SMPL_ARRAY) |
      (t & gs::cnf::PARTYPE_EXT_ARRAY)
    );
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
          PyObject *args = Py_BuildValue("(ssfi)", param.getName().c_str(), param.getString().c_str(), pysc::api::systemc::simulation_time(sc_core::SC_NS), reason);
          PyObject *result = PyObject_CallObject(callback, args);
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
