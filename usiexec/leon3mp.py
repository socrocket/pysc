#!/usr/bin/env python
# vim : set fileencoding=utf-8 expandtab noai ts=4 sw=4 :
# @addtogroup platform
# @{
# @file sc_main.cpp
#
# @date 2010-2014
# @copyright All rights reserved.
#            Any reproduction, use, distribution or disclosure of this
#            program, without the express, prior written consent of the 
#            authors is strictly prohibited.
# @author Rolf Meyer
import usi
from usi.shell import start as shell_start
from usi.systemc import NS as SC_NS

@usi.on('start_of_initialization')
def configuration(*k, **kw):
    from sr_registry import module
    SC_NS = usi.systemc.api.SC_NS

    ncpu = 1
    clk = float(10.0)
    osemu = ""
    log = ""
    power_mon = False
    at_simulation = False
    ambaLayer = False

    #print "AHBCtrl", dir(module)
    ahbctrl = module.AHBCtrl("ahbctrl",
    #    ambaLayer,
        ioaddr = 0xFFF,    # The MSB address of the I/O area
        iomask = 0xFFF,    # The I/O area address mask
        cfgaddr = 0xFF0,   # The MSB address of the configuration area
        cfgmask = 0xFF0,   # The address mask for the configuration area
        rrobin = False,    # 1 - round robin, 0 - fixed priority arbitration (only AT)
        split = False,     # Enable support for AHB SPLIT response (only AT)
        defmast = 0,       # Default AHB master
        ioen = True,       # AHB I/O area enable
        fixbrst = False,   # Enable support for fixed-length bursts (disabled)
        fpnpen = True,     # Enable full decoding of PnP configuration records
        mcheck = True,     # Check if there are any intersections between core memory regions
    #    power = power_mon  # Enable/disable power monitoring
    )

    # Set clock
    #ahbctrl.set_clk(clk, SC_NS)

    apbctrl = module.APBCtrl("apbctrl",
    #    ambaLayer,         # TLM abstraction layer
        bar__0__haddr = 0x800,     # The 12 bit MSB address of the AHB area.
        bar__0__hmask = 0xFFF,     # The 12 bit AHB area address mask
        mcheck = True,     # Check for intersections in the memory map
        hindex = 2,        # AHB bus index
    #    power = power_mon, # Power Monitoring on/off
    )
    #apbctrl.generics.bar[0].haddr.cci_write("0x800")
    #apbctrl.generics.bar[0].hmask.cci_write("0xFFF")

    # Connect to AHB and clock
    ahbctrl.ahbOUT.socket_bind(apbctrl.ahb)
    #apbctrl.set_clk(clk, SC_NS)

    irqmp = module.Irqmp("irqmp",
        paddr = 0x002,    # paddr PSiegl: SoCRocket default 0x1F0, try to mimic TSIM therefore 0x2
        pmask = 0xFFF,     # pmask
        ncpu = ncpu,      # ncpu
        eirq = 0,         # eirq
        pindex = 2,       # pindex
    #    power = power_mon # power monitoring
    )

    # Connect to APB and clock
    apbctrl.apb.socket_bind(irqmp.apb)
    #irqmp.set_clk(clk, SC_NS)

    mctrl = module.Mctrl( "mctrl",
    #    ambaLayer,
        romasel = 28,
        sdrasel = 29,
        romaddr = 0x000,
        rommask = 0xE00,
        ioaddr = 0x200,
        iomask = 0xE00,
        ramaddr = 0x400,
        rammask = 0xC00,
        paddr = 0x000, # APB Base Address
        pmask = 0xFFF, # APB Base Mask
        wprot = 0,
        srbanks = 4,
        ram8 = 1,
        ram16 = 1,
        sepbus = 0,
        sdbits = 32,
        mobile = 0,
        sden = 1,
        hindex = 0,
        pindex = 0,
    #    power = power_mon,
    );

    # Connecting AHB Slave
    ahbctrl.ahbOUT.socket_bind(mctrl.ahb);
    # Connecting APB Slave
    apbctrl.apb.socket_bind(mctrl.apb);
    # Set clock
    #mctrl.set_clk(clk, SC_NS);

    rom = module.Memory("rom",
        type = "0", #"ROM",
        banks = 2,
        bsize = 256 * 1024 * 1024, # bsize * 1024 * 1024
        bits = 32,
        cols = 0,
        storage = "ArrayStorage",
    #    power = power_mon
    )

    # Connect to memory controller and clock
    mctrl.mem.socket_bind(rom.bus)
    #rom.set_clk(clk, SC_NS)

    # IO memory instantiation
    io = module.Memory("io",
        type = "1", #"IO",
        banks = 1,
        bsize = 512 * 1024 * 1024,
        bits = 32,
        cols = 0,
        storage = "MapStorage",
    #    power = power_mon
    )

    # Connect to memory controller and clock
    mctrl.mem.socket_bind(io.bus)
    #io.set_clk(clk, SC_NS)

    # SRAM instantiation
    sram = module.Memory("sram",
        type = "2", #"SRAM",
        banks = 4,
        bsize = 128 * 1024 * 1024,
        bits = 32,
        cols = 0,
        storage = "MapStorage",
    #    power = power_mon
    )

    # Connect to memory controller and clock
    mctrl.mem.socket_bind(sram.bus)
    #sram.set_clk(clk, SC_NS)

    # SDRAM instantiation
    sdram = module.Memory( "sdram",
        type = "3", # "SDRAM",
        banks = 2,
        bsize = 256 * 1024 * 1024,
        bits = 32,
        cols = 16,
        storage = "ArrayStorage",
    #    power = power_mon
    )

    # Connect to memory controller and clock
    mctrl.mem.socket_bind(sdram.bus)
    #sdram.set_clk(clk, SC_NS)


    ahbmem = module.AHBMem("ahbmem",
    #    ambaLayer,
        haddr = 0xA00,
        hmask = 0xFFF,
        hindex = 1,
        cacheable = 1,
        wait_states = 0,
    #    power = power_mon
    )

    # Connect to ahbctrl and clock
    ahbctrl.ahbOUT.socket_bind(ahbmem.ahb)
    #ahbmem.set_clk(clk, SC_NS)
    for i in range(0, ncpu):
      leon3 = module.Leon3("leon3_0", hindex = i)

      # Connecting AHB Master
      leon3.ahb.socket_bind(ahbctrl.ahbIN)
      # Set clock
      #leon3.set_clk(clk, SC_NS)
      leon3.snoop.signal_bind(ahbctrl.snoop)

      irqmp.cpu_req.signal_bind(leon3.cpu.IRQ_port.irq_signal, long(i))
      leon3.cpu.irqAck.ack.signal_bind(irqmp.irq_ack, long(i))
      leon3.cpu.irqAck.run.signal_bind(irqmp.cpu_rst, long(i))
      leon3.cpu.irqAck.status.signal_bind(irqmp.cpu_stat, long(i))

    """
    # CREATE LEON3 Processor
    # ===================================================
    # Always enabled.
    # Needed for basic platform.
    gs::gs_param_array p_mmu_cache("mmu_cache", p_conf);
    gs::gs_param_array p_mmu_cache_ic("ic", p_mmu_cache);
    gs::gs_param<bool> p_mmu_cache_ic_en("en", true, p_mmu_cache_ic);
    gs::gs_param<int> p_mmu_cache_ic_repl("repl", 0, p_mmu_cache_ic);
    gs::gs_param<int> p_mmu_cache_ic_sets("sets", 1, p_mmu_cache_ic);
    gs::gs_param<int> p_mmu_cache_ic_linesize("linesize", 8, p_mmu_cache_ic);
    gs::gs_param<int> p_mmu_cache_ic_setsize("setsize", 4, p_mmu_cache_ic);
    gs::gs_param<bool> p_mmu_cache_ic_setlock("setlock", 1, p_mmu_cache_ic);
    gs::gs_param_array p_mmu_cache_dc("dc", p_mmu_cache);
    gs::gs_param<bool> p_mmu_cache_dc_en("en", true, p_mmu_cache_dc);
    gs::gs_param<int> p_mmu_cache_dc_repl("repl", 0, p_mmu_cache_dc);
    gs::gs_param<int> p_mmu_cache_dc_sets("sets", 1, p_mmu_cache_dc);
    gs::gs_param<int> p_mmu_cache_dc_linesize("linesize", 4, p_mmu_cache_dc);
    gs::gs_param<int> p_mmu_cache_dc_setsize("setsize", 4, p_mmu_cache_dc);
    gs::gs_param<bool> p_mmu_cache_dc_setlock("setlock", 1, p_mmu_cache_dc);
    gs::gs_param<bool> p_mmu_cache_dc_snoop("snoop", 1, p_mmu_cache_dc);
    gs::gs_param_array p_mmu_cache_ilram("ilram", p_mmu_cache);
    gs::gs_param<bool> p_mmu_cache_ilram_en("en", false, p_mmu_cache_ilram);
    gs::gs_param<unsigned int> p_mmu_cache_ilram_size("size", 0u, p_mmu_cache_ilram);
    gs::gs_param<unsigned int> p_mmu_cache_ilram_start("start", 0u, p_mmu_cache_ilram);
    gs::gs_param_array p_mmu_cache_dlram("dlram", p_mmu_cache);
    gs::gs_param<bool> p_mmu_cache_dlram_en("en", false, p_mmu_cache_dlram);
    gs::gs_param<unsigned int> p_mmu_cache_dlram_size("size", 0u, p_mmu_cache_dlram);
    gs::gs_param<unsigned int> p_mmu_cache_dlram_start("start", 0u, p_mmu_cache_dlram);
    gs::gs_param<unsigned int> p_mmu_cache_cached("cached", 0u, p_mmu_cache);
    gs::gs_param<unsigned int> p_mmu_cache_index("index", 0u, p_mmu_cache);
    gs::gs_param_array p_mmu_cache_mmu("mmu", p_mmu_cache);
    gs::gs_param<bool> p_mmu_cache_mmu_en("en", true, p_mmu_cache_mmu);
    gs::gs_param<unsigned int> p_mmu_cache_mmu_itlb_num("itlb_num", 8, p_mmu_cache_mmu);
    gs::gs_param<unsigned int> p_mmu_cache_mmu_dtlb_num("dtlb_num", 8, p_mmu_cache_mmu);
    gs::gs_param<unsigned int> p_mmu_cache_mmu_tlb_type("tlb_type", 1u, p_mmu_cache_mmu);
    gs::gs_param<unsigned int> p_mmu_cache_mmu_tlb_rep("tlb_rep", 1, p_mmu_cache_mmu);
    gs::gs_param<unsigned int> p_mmu_cache_mmu_mmupgsz("mmupgsz", 0u, p_mmu_cache_mmu);
      # AHBMaster - MMU_CACHE
      # =====================
      # Always enabled.
      # Needed for basic platform.
      leon3 = new Leon3(
              sc_core::sc_gen_unique_name("leon3", false), // name of sysc module
              p_mmu_cache_ic_en,         //  int icen = 1 (icache enabled)
              p_mmu_cache_ic_repl,       //  int irepl = 0 (icache LRU replacement)
              p_mmu_cache_ic_sets,       //  int isets = 4 (4 instruction cache sets)
              p_mmu_cache_ic_linesize,   //  int ilinesize = 4 (4 words per icache line)
              p_mmu_cache_ic_setsize,    //  int isetsize = 16 (16kB per icache set)
              p_mmu_cache_ic_setlock,    //  int isetlock = 1 (icache locking enabled)
              p_mmu_cache_dc_en,         //  int dcen = 1 (dcache enabled)
              p_mmu_cache_dc_repl,       //  int drepl = 2 (dcache random replacement)
              p_mmu_cache_dc_sets,       //  int dsets = 2 (2 data cache sets)
              p_mmu_cache_dc_linesize,   //  int dlinesize = 4 (4 word per dcache line)
              p_mmu_cache_dc_setsize,    //  int dsetsize = 1 (1kB per dcache set)
              p_mmu_cache_dc_setlock,    //  int dsetlock = 1 (dcache locking enabled)
              p_mmu_cache_dc_snoop,      //  int dsnoop = 1 (dcache snooping enabled)
              p_mmu_cache_ilram_en,      //  int ilram = 0 (instr. localram disable)
              p_mmu_cache_ilram_size,    //  int ilramsize = 0 (1kB ilram size)
              p_mmu_cache_ilram_start,   //  int ilramstart = 8e (0x8e000000 default ilram start address)
              p_mmu_cache_dlram_en,      //  int dlram = 0 (data localram disable)
              p_mmu_cache_dlram_size,    //  int dlramsize = 0 (1kB dlram size)
              p_mmu_cache_dlram_start,   //  int dlramstart = 8f (0x8f000000 default dlram start address)
              p_mmu_cache_cached,        //  int cached = 0xffff (fixed cacheability mask)
              p_mmu_cache_mmu_en,        //  int mmu_en = 0 (mmu not present)
              p_mmu_cache_mmu_itlb_num,  //  int itlb_num = 8 (8 itlbs - not present)
              p_mmu_cache_mmu_dtlb_num,  //  int dtlb_num = 8 (8 dtlbs - not present)
              p_mmu_cache_mmu_tlb_type,  //  int tlb_type = 0 (split tlb mode - not present)
              p_mmu_cache_mmu_tlb_rep,   //  int tlb_rep = 1 (random replacement)
              p_mmu_cache_mmu_mmupgsz,   //  int mmupgsz = 0 (4kB mmu page size)>
              p_mmu_cache_index + i,     // Id of the AHB master
              p_report_power,            // Power Monitor,
              ambaLayer                  // TLM abstraction layer
      )

"""
    gptimer = module.GPTimer("gptimer",
        ntimers = 2,
        pindex = 3,
        paddr = 0x003,
        pmask = 0xFFF,
        pirq = 8,
        sepirq = True,
        sbits = 16,
        nbits = 32,
        wdog = 1,
    #    power = power_mon
    )

    # Connect to apb and clock
    apbctrl.apb.socket_bind(gptimer.apb)
    #gptimer.set_clk(clk, SC_NS)

    # Connecting Interrupts
    for i in range(0, 8):
        irqmp.irq_in.signal_bind(gptimer.irq, 8 + i)

    apbuart = module.APBUART("apbuart0",
        backend = "ReportIO",
        pindex = 1,
        paddr = 0x001,
        pmask = 0xFFF,
        pirq = 2,
    #    power = power_mon
    )

    # Connecting APB Slave
    apbctrl.apb.socket_bind(apbuart.apb)
    # Connecting Interrupts
    irqmp.irq_in.signal_bind(apbuart.irq, 2)
    # Set clock
    #apbuart.set_clk(clk, SC_NS)

    apbuart = module.APBUART("apbuart1",
        backend = "ReportIO",
        pindex = 9,
        paddr = 0x009,
        pmask = 0xFFF,
        pirq = 3,
    #    power = power_mon
    )

    # Connecting APB Slave
    apbctrl.apb.socket_bind(apbuart.apb)
    # Connecting Interrupts
    irqmp.irq_in.signal_bind(apbuart.irq, 3)
    # Set clock
    #apbuart.set_clk(clk,SC_NS)

    #ahbprof = module.AHBProf("ahbprof",
    #    ambaLayer,
    #    hindex = 6,
    #    haddr = 0x900,
    #    hmask = 0xFFF
    #)

    # Connecting APB Slave
    #ahbctrl.ahbOUT.socket_bind(ahbprof.ahb)
    #ahbprof.set_clk(clk, SC_NS)

    reset = module.ResetIrqmp("reset")
    irqmp.rst.signal_bind(reset.rst)

    #shell_start()

