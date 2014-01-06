#ifndef SCRIPT_H
#define SCRIPT_H

// SystemC library
#include <systemc>

// forward declaration
struct _object;
typedef struct _object PyObject;
struct _ts;
typedef struct _ts PyThreadState;

class PythonModule: public sc_core::sc_module {
  public:
    PythonModule(
      sc_core::sc_module_name name,
      const char* script_filename = 0,
      int argc = 0, char **argv = NULL);

    virtual ~PythonModule();

    void execfile(const char* script_filename);

    /// runs a Python command in a module-specific  namespace
    void exec(const char* statement);

    /// Adds a path to the load/import search path
    void add_to_pythonpath(const char* path);

    void start_of_initialization();
    void end_of_initialization();
    void start_of_elaboration();
    void end_of_elaboration();
    void start_of_simulation();
    void end_of_simulation();
    void start_of_evaluation();
    void end_of_evaluation();

  private:
    /// internal load functionality
    bool private_load(const char *fullname);

    /// Set interpreter name in the script namespace
    void set_interpreter_name();

    /// Runs a Python function from the script module
    void run_py_member(const char* name);

    bool initialised;
    PyObject *my_namespace, *pysc_module, *sys_path, *name_py;

    /// Number of subscriber to the singlton python instance
    static unsigned subscribers;

    /// The singleton python thread
    static PyThreadState *singleton;

    /// OS Path seperator. Should come from boost
    static std::string path_separator();

    /// Check if path is just a file name
    static bool is_simple_filename(const char *path);

    /// Block out singleton thread
    /// This should not be neccesarry but who knows
    static void block_threads();

    /// Unblock our singleton thread
    static void unblock_threads();

    /// Subscribe new PythonModule to thread
    static void subscribe();

    /// Unsubscribe from the thread
    static void unsubscribe();
};

#endif


