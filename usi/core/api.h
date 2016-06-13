// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup pysc
/// @{
/// @file api.h
///
/// @date 2013-2015
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the
///            authors is strictly prohibited.
/// @author Rolf Meyer
#ifndef PYSC_USI_CORE_API_H_
#define PYSC_USI_CORE_API_H_

extern "C" {
#if ! defined(_object)
struct _object;
typedef struct _object PyObject;
#endif
#if ! defined(_ts)
struct _ts;
typedef struct _ts PyThreadState;
#endif
#if ! defined(_is)
struct _is;
typedef struct _is PyInterpreterState;
#endif
};

typedef PyObject * PyScObject;

/// Initialize the USI Python environment.
/// Take the application argc argv arguments to provide them to the python script.
/// Therefore the scripting environment can be used to initialize the simulation.
/// @param argc Number of arguments
/// @param argv List of arguments
void pysc_init(int argc, char *argv[]);

/// Load a python script by file path or module name.
/// This function instructs the USI Pythn environment to execute a python script.
/// The script can be either provided as a file path ending with the file extension .py.
/// Or it can be a hierachial python module path rooted in the SoCRocket top level directory or
/// linked into the site-packages of the venv of SoCRocket.
/// @param module Module name or path.
void pysc_load(const char *module);

/// This function marks the begin of the initialization.
/// It will call all python functions registered to this phase.
void pysc_start_of_initialization();

/// This function marks the end of the initialization.
/// It will call all python dunctions registered to this phase.
void pysc_end_of_initialization();

/// Starts the simulation.
/// This is a wrapper for sc_start.
/// It extens the simulation environment with the capapbility to react on simulation interruptions.
/// Therefore if the user presses Ctrl-c during simulation or sc_pause() is executed during simulation
/// all scripts registered to the phase pause_of_simulation are executed until the simulation will be started again.
void pysc_start();
void pysc_start(const sc_time& duration, sc_starvation_policy p = SC_RUN_TO_TIME);
void pysc_start(double duration, sc_time_unit unit, sc_starvation_policy p = SC_RUN_TO_TIME);

/// The signal handler for the python environment.
/// It should be registered in order to use system signals with the simulation.
/// @param sig the signal sent to the process.
void pysc_signal_handler(int sig);

#endif  // PYSC_USI_CORE_API_H_
/// @}

