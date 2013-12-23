#include "pysc/api/gc.h"
#include "pysc/module.h"

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

/*
// functions for parameter object creation //
// globals used to pass C++ pointers from Python to constructors
static ParamArray *array_parent = 0;
static ExtParamArray *ext_array_parent = 0;
static Param *current_param = 0;

Param::Param(std::string name, std::string default_val) {
    // constructor for a standalone param or a param child of an extended array.
    // if a child, the parent is found in a global variable
    if(ext_array_parent != 0) {
        gs::gs_param_array *parent = ext_array_parent->getParam();
        m_param = new gs::gs_param<std::string>(name, default_val, parent);
        m_has_parent = true;
    } else {
        m_param = new gs::gs_param<std::string>(name, default_val);
        m_has_parent = false;
    }
    m_is_array_element = false;
    ext_array_parent = 0;
    array_parent = 0;
}

Param::Param(unsigned index, std::string default_val) {
    // constructor for a param child of a simple array.  parent is in a global.
    // makes this into a std::string.  in this case all
    // get/set go through the parent, default val is used only if the parent
    // notes that the size from the dB is smaller than the index, and then
    // the default val should also be applied to the dB.
    assert(array_parent != 0);
    gs::gs_param<std::string *> *parent = array_parent->getParam();
    if(parent->size() <= index) {
        parent->resize(index+1);
    }
    if(array_parent->db_size() <= index) {
        (*parent)[index] = default_val;
    }
    m_is_array_element = true;
    m_has_parent = false;
    m_parent = parent;
    m_index_in_array = index;
    ext_array_parent = 0;
    array_parent = 0;
}

Param::~Param() {
    if((!m_is_array_element) && (!m_has_parent)) {
        delete m_param;
    }
}

std::string Param::get() {
    if(m_is_array_element) {
        return (*m_parent)[m_index_in_array];
    }
    return m_param->getValue();
}

void Param::set(std::string val) {
    if(m_is_array_element) {
        (*m_parent)[m_index_in_array] = val;
    } else {
        m_param->setValue(val);
    }
}

void Param::set_param_as_current() {
    current_param = this;
}


ParamArray::ParamArray(std::string name) {
    // constructor for a standalone array param or an array param child
    // of an extended array.  if a child, the parent is in a global variable
    if(ext_array_parent != 0) {
        gs::gs_param_array *parent = ext_array_param->getParam();
        m_param = new gs::gs_param<std::string *>(name, parent);
        m_has_parent = true;
    } else {
        m_param = new gs::gs_param<std::string *>(name);
        m_has_parent = false;
    }
    m_length_from_db = m_param->size();
    ext_array_parent = 0;
    array_parent = 0;
}

ParamArray::ParamArray(unsigned index) {
    // constructor for a child of a simple array and will fail
    // with the current version of GreenConfig.  parent is found in a global
    assert(false);
    ext_array_parent = 0;
    array_parent = 0;
}

ParamArray::~ParamArray() {
    if(!m_has_parent) {
        delete m_param;
    }
}

unsigned ParamArray::length() {
  return m_param->size();
}

unsigned ParamArray::db_length() {
    return m_length_from_db;
}

void ParamArray::length(unsigned length) {
    m_param->resize(length);
}

void ParamArray::make_parent() {
    // function to call before the construction of a child param
    array_parent = this;
}


ExtParamArray::ExtParamArray(std::string name) {
    // constructor for a standalone param or a param child of an extended array.
    // if a child, the parent is found in a global variable
    if(ext_array_parent != 0) {
        gs::gs_param_array *parent = ext_array_parent->getParam();
        m_param = new gs::gs_param_array(name, parent);
        m_has_parent = true;
    } else {
        m_param = new gs::gs_param_array(name);
        m_has_parent = false;
    }
    ext_array_parent = 0;
    array_parent = 0;
}

ExtParamArray::ExtParamArray(unsigned index) {
    // constructorfor a child of a simple array and will fail
    // with the current version of GreenConfig.  parent is found in a global
    // function to call before the construction of a child param
    assert(false);
    ext_array_parent = 0;
    array_parent = 0;
}

ExtParamArray::~ExtParamArray() {
    if(!m_has_parent) delete m_param;
}

void ExtParamArray::make_parent() {
    ext_array_parent = this;
}
*/  
}; // gc
}; // api
}; // pysc
