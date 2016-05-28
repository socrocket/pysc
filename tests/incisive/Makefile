CDSROOT=$(shell ncroot)
CCFLAGS=-DLONG_BIT=32

PWD=$(shell pwd)
SOCROCKET_ROOT=$(shell readlink -f $(PWD)/../../..)
INTINCLUDES=-I$(SOCROCKET_ROOT) -I$(SOCROCKET_ROOT)/pysc -I.
DEPINCLUDES=-I$(SOCROCKET_ROOT)/build/.conf_check_deps/dist/greenlib-trunk/greencontrol/include
CDSINCLUDES=-I$(CDSROOT)/tools/systemc/include_pch -I$(CDSROOT)/tools/tbsc/include -I$(CDSROOT)/tools/vic/include -I$(CDSROOT)/tools/systemc/include/cci -I$(CDSROOT)/tools/systemc/include/factory -I$(CDSROOT)/tools/systemc/include/tlm2
INCLUDES=$(INTINCLUDES) $(CDSINCLUDES) $(DEPINCLUDES)

#PYTHONFLAGS=-I/usr/include/python2.7 -L/usr/lib -lpthread -ldl -lutil -lm -lpython2.7
#PYTHONFLAGS=-I$(CDSROOT)/tools/python279/include/python2.7 -L$(CDSROOT)/tools/python279/lib -lpthread -ldl -lutil -lm -lpython2.7
PYTHONFLAGS=-I/usr/include/python2.7 -L/usr/lib -lpthread -ldl -lutil -lm -lpython2.7

#PYSWIG=swig -c++ -python -Wall -Ipysc -I. -I/usr/include -Ibuild/.conf_check_deps/dist/systemc-2.3.0/include -I/usr/include/python2.7 -DPYTHONDIR="/usr/lib/python2.7/site-packages" -DPYTHONARCHDIR="/usr/lib64/python2.7/site-packages" -DLITTLE_ENDIAN_BO -D_REENTRANT -DUSE_STATIC_CASTS -DSC_INCLUDE_DYNAMIC_PROCESSES -DSC_USE_PTHREADS 
PYSWIG=swig -c++ -python -Wall $(INCLUDES) -DPYTHONDIR="/usr/lib/python2.7/site-packages" -DPYTHONARCHDIR="/usr/lib64/python2.7/site-packages" -DLITTLE_ENDIAN_BO -D_REENTRANT -DUSE_STATIC_CASTS -DSC_INCLUDE_DYNAMIC_PROCESSES -DSC_USE_PTHREADS 

CDSWORK=build/objs/

CDSCC=$(CDSROOT)/tools/cdsgcc/gcc/bin/g++
#CDSCC=g++
CDSCCFLAGS=$(CCFLAGS) $(PYTHONFLAGS) $(INCLUDES) -c -x c++ -m32 -Wall
#CDSLDFLAGS=$(CCFLAGS) $(PYTHONFLAGS) $(INCLUDES) -Wl,-m=elf_i386 -m32 -Wall
CDSLDFLAGS=$(CCFLAGS) $(PYTHONFLAGS) $(INCLUDES) -m32 -Wall

#SOURCE=../../../core/common/sr_register/scireg.cpp ../../../core/common/sr_registry/sr_registry.cpp ../../../pysc/usi/core/api.cpp ../../../pysc/usi/core/module.cpp ../../../pysc/tests/questasim/tlm2_getting_started_1.cpp ../../../pysc/usi/api/systemc.cpp
SOURCE=$(SOCROCKET_ROOT)/core/common/waf.cpp $(SOCROCKET_ROOT)/core/common/sr_report/sr_report.cpp $(SOCROCKET_ROOT)/core/common/sr_registry/sr_registry.cpp $(SOCROCKET_ROOT)/pysc/usi/core/registry.cpp $(SOCROCKET_ROOT)/pysc/usi/core/api.cpp $(SOCROCKET_ROOT)/pysc/usi/core/module.cpp $(SOCROCKET_ROOT)/pysc/usi/api/systemc.cpp
#SOURCE=core/common/scireg.cpp pysc/tests/questasim/tlm2_getting_started_1.cpp pysc/usi/api/systemc.cpp

SWIGIF=$(SOCROCKET_ROOT)/core/common/sr_report/sr_report.i $(SOCROCKET_ROOT)/core/common/sr_registry/sr_registry.i $(SOCROCKET_ROOT)/pysc/usi/api/systemc.i $(SOCROCKET_ROOT)/pysc/usi/api/delegate.i $(SOCROCKET_ROOT)/core/common/sr_register/scireg.i


all: cadence

cadence: libncsc_model.so

$(CDSWORK).build:
	@-mkdir -p $(CDSWORK) && touch $(CDSWORK).build

clean:
	-rm -r $(QUESTAWORK)
	-rm -r $(TCLWORK)

mscireg: scireg/main.cpp build/usi.a
	#ncsc_run $^ -tcl -top Top -Wl,--no-as-needed $(INCLUDES) -lpython2.7 -lboost_system -lboost_filesystem
	ncsc_run -stop elab scireg/main.cpp build/usi.a -Wl,--no-as-needed $(INCLUDES) -lpython2.7 -lboost_system -lboost_filesystem -Iscireg -DSC_INCLUDE_FX

tlm: tlm2_getting_started_1.cpp build/usi.a
	#ncsc_run $^ -tcl -top Top -Wl,--no-as-needed $(INCLUDES) -lpython2.7 -lboost_system -lboost_filesystem
	ncsc_run -stop elab $^ -Wl,--no-as-needed $(INCLUDES) -lpython2.7 -lboost_system -lboost_filesystem

build/usi.a: $(patsubst %.cpp, $(CDSWORK)%.o, $(notdir $(SOURCE))) $(patsubst %.i, $(CDSWORK)%.swig.o, $(notdir $(SWIGIF)))
	#$(CDSCC) $(INCLUDES) -Wl,-Bstatic -o $@ $<
	#$(CDSCC) $(CDSLDFLAGS) $(INCLUDES) -Wl,--verbose -o $@ $^
	ar rcs -o $@ $^

define cdsswig_obj
$(addprefix $(CDSWORK), $(notdir $(1:%.i=%.swig.cpp))): $(1) $(CDSWORK).build
	$$(PYSWIG) -o $$@ $$<

$(addprefix $(CDSWORK), $(notdir $(1:%.i=%.swig.o))): $(addprefix $(CDSWORK), $(notdir $(1:%.i=%.swig.cpp))) $(CDSWORK).build
	$$(CDSCC) $$(CDSCCFLAGS) -o $$@ $$<

endef

define cdscc_obj
$(addprefix $(CDSWORK), $(notdir $(1:%.cpp=%.o))): $(1) $(CDSWORK).build
	$$(CDSCC) $$(CDSCCFLAGS) -o $$@ $$<

endef

$(foreach src, $(SOURCE), $(eval $(call cdscc_obj, $(src))))
$(foreach src, $(SWIGIF), $(eval $(call cdsswig_obj, $(src))))
