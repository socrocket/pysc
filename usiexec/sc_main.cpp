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
#include "gaisler/leon3/leon3.h"
#include "gaisler/ahbin/ahbin.h"
#include "gaisler/memory/memory.h"
#include "gaisler/apbctrl/apbctrl.h"
#include "gaisler/ahbmem/ahbmem.h"
#include "gaisler/mctrl/mctrl.h"
#include "gaisler/leon3/mmucache/defines.h"
#include "gaisler/gptimer/gptimer.h"
#include "gaisler/apbuart/apbuart.h"
#include "gaisler/apbuart/tcpio.h"
#include "gaisler/apbuart/reportio.h"
#include "gaisler/irqmp/irqmp.h"
#include "gaisler/ahbctrl/ahbctrl.h"
#include "gaisler/ahbprof/ahbprof.h"
#include "models/voter/voter.h"
#include "models/commitregister/commitregister.h"
#include <boost/filesystem.hpp>

#ifdef HAVE_SOCWIRE
#include "models/socwire/AHB2Socwire.h"
#endif
#ifdef HAVE_GRETH
#include "models/greth/greth/greth.h"
#include "vphy/tapdev.h"
#include "vphy/loopback.h"
#endif
#ifdef HAVE_AHBDISPLAY
#include "models/ahbdisplay/ahbdisplay.h"
#endif
#ifdef HAVE_AHBCAMERA
#include "models/ahbcamera/ahbcamera.h"
#endif
#ifdef HAVE_AHBSHUFFLER
#include "models/ahbshuffler/ahbshuffler.h"
#endif
#ifdef HAVE_AHBGPGPU
#include "ahbgpgpu/models/nyuzi/nyuzi.h"
#endif /* #ifdef HAVE_AHBGPGPU */

//#include "vphy/trafgen.h"

using namespace std;
using namespace sc_core;
#ifdef HAVE_SOCWIRE
using namespace socw;
#endif

extern int exitValue;

void stopSimFunction(int sig) {
  v::warn << "main" << "Simulation interrupted by user" << std::endl;
  sc_core::sc_stop();
  wait(SC_ZERO_TIME);
}

int sc_main(int argc, char** argv) {
    sr_report_handler::handler = sr_report_handler::default_handler;

    gs::ctr::GC_Core core;
    gs::cnf::ConfigDatabase cnfdatabase("ConfigDatabase");
    gs::cnf::ConfigPlugin configPlugin(&cnfdatabase);

    //SR_INCLUDE_MODULE(ArrayStorage);
    //SR_INCLUDE_MODULE(MapStorage);
    //SR_INCLUDE_MODULE(ReportIO);
    //SR_INCLUDE_MODULE(TcpIO);

    //SR_INCLUDE_MODULE(Memory);
    //SR_INCLUDE_MODULE(Mctrl);
    //SR_INCLUDE_MODULE(AHBCtrl);
    //SR_INCLUDE_MODULE(APBCtrl);
    //SR_INCLUDE_MODULE(Irqmp);
    //SR_INCLUDE_MODULE(GPTimer);
    //SR_INCLUDE_MODULE(AHBMem);
    //SR_INCLUDE_MODULE(AHBProf);
    //SR_INCLUDE_MODULE(APBUART);
    SR_INCLUDE_MODULE(Leon3);
    SR_INCLUDE_MODULE(MicroBlaze);
    //SR_INCLUDE_MODULE(ResetIrqmp);
    SR_INCLUDE_MODULE(Voter);
    SR_INCLUDE_MODULE(CommitRegister);

#ifdef HAVE_USI
    // Initialize Python
    USI_HAS_MODULE(systemc);
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
    //(void) signal(SIGINT, stopSimFunction);
    //(void) signal(SIGTERM, stopSimFunction);
    usi_end_of_initialization();
    usi_start();
#endif  // HAVE_USI

    //amba::amba_layer_ids ambaLayer;
    //    ambaLayer = amba::amba_AT;
    //    ambaLayer = amba::amba_LT;
    //
    return 0;
}
/// @}
