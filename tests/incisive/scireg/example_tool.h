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

//
// This file contains an example tool which demonstrates usage of the SCIREG API .
//

#ifndef EXAMPLE_TOOL_H
#define EXAMPLE_TOOL_H

namespace scireg_ns {

void example_print(scireg_region_if & region, std::ostream& os, const char* indent, const char* name, sc_dt::uint64 offset)
{
    scireg_region_type region_type;
    if (region.scireg_get_region_type(region_type) != SCIREG_SUCCESS)
      return;

    if (region_type == SCIREG_REGISTER)
    {
      os << indent << "register: name: " << name << "\n";
      os << indent << "register: offset: " << offset << "\n";
      os << indent << "register: byte width: " << region.scireg_get_byte_width() << "\n";
      os << indent << "register: value: " ;
      vector_byte v;
      vector_byte::iterator it;
      unsigned cnt;
      if (region.scireg_read(v, region.scireg_get_byte_width()) == SCIREG_SUCCESS)
        for (it = v.begin(), cnt = 0; cnt < region.scireg_get_byte_width();  ++it, ++cnt)
          os << std::hex << unsigned(v[cnt]) << std::dec << " " ;
      os << indent << "\n";

      os << indent << "register: bit_width: " << region.scireg_get_bit_width() << "\n";

      std::vector<sc_core::sc_module*> vm;
      if ((region.scireg_get_parent_modules(vm) == SCIREG_SUCCESS) && (vm.size() > 0))
        os << indent << "register: parent module: " << vm[0]->name() << "\n";

      std::vector<scireg_mapped_region> mapped_regions;
      std::vector<scireg_mapped_region>::iterator it_reg;
      std::string indent2(::std::string("   ") + indent);

      region.scireg_get_child_regions(mapped_regions);
      for (it_reg = mapped_regions.begin(); it_reg != mapped_regions.end(); ++it_reg)
      {
        os << indent << "child field: \n" ;
        example_print(*(*it_reg).region, os, indent2.c_str(), "", 0);
      }
    }

    if (region_type == SCIREG_BANK)
    {  
      os << indent << "bank: name: " << name << "\n";
      os << indent << "bank: offset: " << offset << "\n";
      os << indent << "bank: byte width: " << region.scireg_get_byte_width() << "\n";
      std::vector<scireg_mapped_region> mapped_regions;
      std::vector<scireg_mapped_region>::iterator it_reg;
      std::string indent2(::std::string("   ") + indent);

      region.scireg_get_child_regions(mapped_regions);
      for (it_reg = mapped_regions.begin(); it_reg != mapped_regions.end(); ++it_reg)
      {
        os << indent << "child region: \n" ;
        example_print(*(*it_reg).region, os, indent2.c_str(), (*it_reg).name, (*it_reg).offset);
      }
    }

    if (region_type  == SCIREG_FIELD)
    {
      const char *s;
      if (region.scireg_get_string_attribute(s, SCIREG_NAME) == SCIREG_SUCCESS)
        os << indent << "register field: name: " << s << "\n";

      os << indent << "register field: low_pos: " << region.scireg_get_low_pos() << "\n";
      os << indent << "register field: high_pos: " << region.scireg_get_high_pos() << "\n";
      os << indent << "register field: value: " ;
      vector_byte v;
      vector_byte::iterator it;
      unsigned cnt;
      if (region.scireg_read(v, region.scireg_get_byte_width()) == SCIREG_SUCCESS)
        for (it = v.begin(), cnt = 0; cnt < region.scireg_get_byte_width();  ++it, ++cnt)
          os << std::hex << unsigned(v[cnt]) << std::dec << " " ;
      os << indent << "\n";
      return; 
    }
}



class example_callback : public scireg_callback
{
public:
  std::ostream* osp;

  void do_callback(scireg_region_if & r)
  {
     *osp << "Example tool: region accessed at time " << sc_core::sc_time_stamp() << std::endl;
     const char *s = "";
     r.scireg_get_string_attribute(s, SCIREG_NAME);
     example_print(r, *osp, "  ", s, 0);
  }
};

// An example of a tool that tracks all registers and register banks in the design

class example_tool : public scireg_notification_if
{
public:

  virtual void add_region(scireg_region_if & r) { all_scireg_regions.push_back(&r); };
  virtual void remove_region(scireg_region_if & r) {}

  typedef std::vector<scireg_region_if*> scireg_region_vector;

  scireg_region_vector all_scireg_regions;
  
  typedef std::vector<std::pair<example_callback *, scireg_region_if *> > callback_vector;
  
  callback_vector all_scireg_callbacks;
  
  example_tool()
  {
    scireg_ns::scireg_tool_registry::add_tool(*this);
  }
  
  ~example_tool()
  {
     
    // Remove and deallocate all callback objects
    for (callback_vector::iterator it = all_scireg_callbacks.begin();
         it != all_scireg_callbacks.end();
         ++it)
    {
      (*it).second->scireg_remove_callback(*(*it).first);
      
      delete (*it).first;
    }
    
    scireg_ns::scireg_tool_registry::remove_tool(*this);
  }

  void print_regions(::std::ostream& os)
  {
    scireg_region_vector::iterator it;

    for (it = all_scireg_regions.begin(); it != all_scireg_regions.end(); ++it)
    {
      scireg_region_type t;
      if (((*it)->scireg_get_region_type(t) == SCIREG_SUCCESS ) && (t == SCIREG_BANK))
      {
        os << "example_tool:: printing register bank:\n";
        const char *s = "";
        (*it)->scireg_get_string_attribute(s, SCIREG_NAME);
        example_print(*(*it), os, "  ", s, 0);
      }
    }
  }

  void set_callbacks_all_registers(::std::ostream& os)
  {
    osp = &os;

    scireg_region_vector::iterator it;
    for (it = all_scireg_regions.begin(); it != all_scireg_regions.end(); ++it)
    {
       example_callback* cb = new example_callback();
       cb->type = SCIREG_WRITE_ACCESS;
       cb->osp = osp;
       if ((*it)->scireg_add_callback(*cb) == SCIREG_SUCCESS)
         all_scireg_callbacks.push_back(std::make_pair(cb, (*it)));
       else
         delete cb;
    }
  }

protected:
  std::ostream* osp;
};

}

#endif

