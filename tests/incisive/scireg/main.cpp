/*
   Copyright 2011-2012 Cadence Design Systems, Inc.
   Copyright 2011-2012 STMicroelectronics

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/


// This is a simple SystemC example that demonstrates usage of the SCIREG API.
// This example is NOT part of the SCIREG API standard.


#define SC_REGISTER_H 1

#include <sstream>
#include <string>
#include <map>

#include "systemc"
//#include "sysc/communication/sc_register.h"
#include "sc_register.h"
#include "example_tool.h"

//#include "scireg.cpp"
#include "sysc/communication/scireg.h"
#include "usi.h"

using namespace sc_register_example;
using sc_core::SC_ID_ASSERTION_FAILED_;

// An example a register with a number of fields

template<typename T, sc_register_access_mode M>
class uartDR_reg : public sc_register<T,M>
{   
public:
    sc_register_field<T,11,11> OE;
    sc_register_field<T,10,10> BE;
    sc_register_field<T,9,9> PE;
    sc_register_field<T,8,8> FE;
    sc_register_field<T,7,0> DATA;

    // The Constructor 
    uartDR_reg( const char* nm, const T& v, const char* d)
        : sc_register<T,M>(nm, v, d),
          OE("OE", this, ""),
          BE("BE", this, ""),
          PE("PE", this, ""),
          FE("FE", this, ""),
          DATA("DATA", this, "")
    {
      OE.add_value_code(0x0, "NoOverRun");
      OE.add_value_code(0x1, "OverRun");

      BE.add_value_code(0x0, "NoErr");
      BE.add_value_code(0x1, "BreakErr", "");
    }
};  

// An example register bank that contains 3 registers

class my_reg_bank : public sc_register_bank<unsigned long long, unsigned>
{
public:
  my_reg_bank(const char* name, int size) : 
    sc_register_bank<unsigned long long, unsigned>(name, size)
    , reg_a("reg_a", 0xC001C0FE) 
    , reg_b("reg_b", 0xDEADBEEF) 
    , reg_c("reg_c", 0, "") 
  {
    m_registers.push_back(&reg_a);
    m_reg_addr_map[&reg_a] = 0;

    m_registers.push_back(&reg_b);
    m_reg_addr_map[&reg_b] = 4;

    m_registers.push_back(&reg_c);
    m_reg_addr_map[&reg_c] = 8;
  }

  sc_register<unsigned short, SC_REG_RW_ACCESS> reg_a;
  sc_register<unsigned short, SC_REG_RW_ACCESS> reg_b;
  uartDR_reg<unsigned short, SC_REG_RW_ACCESS>  reg_c;

  bool bus_read(unsigned long long, unsigned& i) const { return false; }
  bool bus_write(unsigned long long, unsigned) { return false; }
  bool bus_read_dbg(unsigned long long, unsigned& i) const { return false; }
  bool bus_read_dbg(unsigned long long, unsigned) { return false; }
  bool bus_write_dbg(unsigned long long, unsigned) { return false; }
  bool is_valid_offset(unsigned long long) const { return false; }
  bool supports_action_type(unsigned long long, sc_register_access_type) { return false; }

  const sc_register_vec& get_registers() const { return m_registers; }

  sc_register_base* get_register(const unsigned long long offset)
  {
    switch (offset) {
        case 0:
            return (&(this->reg_a));

        case 4:
            return (&(this->reg_b));

        case 8:
            return (&(this->reg_c));
    }

    return 0;
  }

  bool get_offset(sc_register_base* reg, unsigned long long& offset) const
 {   
    if (reg == NULL) {
        return (false);
    }
    ::std::map<sc_register_base*,unsigned long long>::const_iterator item;
    item = m_reg_addr_map.find(reg);
    if (item == m_reg_addr_map.end()) {
        return (false);
    }
    offset = item->second;
    return (true);
 }

protected:
   sc_register_vec m_registers;
   ::std::map<sc_register_base*,unsigned long long> m_reg_addr_map;
};


// A top level module that instantiates the register bank and writes to the registers during simulation

class top : public sc_core::sc_module
{
public:
  SC_HAS_PROCESS(top);
  top(sc_core::sc_module_name name) : sc_core::sc_module(name), reg_bank("reg_bank", 1000)
  {
    SC_THREAD(main);
  }

  my_reg_bank reg_bank;

  void main()
  {
    sc_core::wait(10, sc_core::SC_NS);

    reg_bank.reg_a.write(2);
    reg_bank.reg_b.write(5);

    sc_core::wait(10, sc_core::SC_NS);
    reg_bank.reg_c.write(8);
  }
};

int sc_main(int argc, char** argv) {
    // Create an instance of the example_tool for the SCIREG API and ask to receive notifications

  USI_HAS_MODULE(systemc);
  USI_HAS_MODULE(delegate);
  USI_HAS_MODULE(sr_registry);
  USI_HAS_MODULE(sr_report);
  USI_HAS_MODULE(scireg);
  usi_init(argc, argv);

  usi_load("usi.api.systemc");
  usi_load("usi.api.delegate");
  usi_load("sr_register.scireg");
  usi_load("testusi");

  usi_start_of_initialization();
    top* t = new top("top");


    usi_start();//(sc_core::sc_time(1000, sc_core::SC_NS));
    
    delete t;

    return (0);
}
