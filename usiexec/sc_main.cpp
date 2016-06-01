// vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
/// @addtogroup platform
/// @{
/// @file sc_main.cpp
///
/// @date 2010-2014
/// @copyright All rights reserved.
///            Any reproduction, use, distribution or disclosure of this
///            program, without the express, prior written consent of the 
///            authors is strictly prohibited.
/// @author Thomas Schuster
///
#ifdef HAVE_USI
#include "pysc/usi.h"
#endif

#include "core/common/sr_param.h"
#include "core/common/systemc.h"
#include <string.h>
#include <sys/time.h>
#include <time.h>
#include <string.h>
#include <mcheck.h>
#include "core/common/amba.h"
#include "core/common/trapgen/debugger/GDBStub.hpp"
#include <iostream>
#include <vector>
#include <cstring>
#include <cstdlib>
#include <stdexcept>

#include "core/common/verbose.h"
#include <boost/filesystem.hpp>

using namespace std;
using namespace sc_core;

int sc_main(int argc, char** argv) {
    sr_report_handler::handler = sr_report_handler::default_handler;

    gs::ctr::GC_Core core;
    gs::cnf::ConfigDatabase cnfdatabase("ConfigDatabase");
    gs::cnf::ConfigPlugin configPlugin(&cnfdatabase);

    // Initialize Python
    USI_HAS_MODULE(systemc);
    USI_HAS_MODULE(sc_module);
    USI_HAS_MODULE(sr_registry);
    USI_HAS_MODULE(delegate);
    USI_HAS_MODULE(intrinsics);
    USI_HAS_MODULE(greensocket);
    USI_HAS_MODULE(scireg);
    USI_HAS_MODULE(amba);
    USI_HAS_MODULE(sr_report);
    USI_HAS_MODULE(sr_signal);
    USI_HAS_MODULE(cci);
    USI_HAS_MODULE(mtrace);
    usi_init(argc, argv);
    //sr_report_handler::handler = sr_report_handler::default_handler; <<-- Uncoment for C++ handler


    // Core APIs will be loaded by usi_init:
    // usi, usi.systemc, usi.api.delegate, usi.api.report
    usi_load("usi.api.greensocket");
    usi_load("sr_register.scireg");
    usi_load("sr_signal.sr_signal");
    usi_load("usi.api.amba");

    usi_load("usi.log");
    usi_load("usi.tools.args");
    usi_load("usi.cci");
    //usi_load("tools.python.power");
    usi_load("usi.shell");
    usi_load("usi.tools.execute");
    usi_load("usi.tools.elf");

    usi_start_of_initialization();
    usi_end_of_initialization();
    usi_start();
    return 0;
}
/// @}
