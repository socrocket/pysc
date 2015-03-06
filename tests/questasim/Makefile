INCLUDES=-I. -Ipysc

PYTHONFLAGS=-m32 -I/lscratch/rmeyer/python-2.7.9-32bit/include/python2.7 -L/lscratch/rmeyer/python-2.7.9-32bit/lib -lpthread -ldl -lutil -lm -lpython2.7
PYSWIG=swig -c++ -python -Wall -Ipysc -I. -I/usr/include -Ibuild/.conf_check_deps/dist/systemc-2.3.0/include -I/usr/include/python2.6 -DPYTHONDIR="/usr/local/lib/python2.6/site-packages" -DPYTHONARCHDIR="/usr/local/lib64/python2.6/site-packages" -DLITTLE_ENDIAN_BO -D_REENTRANT -DUSE_STATIC_CASTS -DSC_INCLUDE_DYNAMIC_PROCESSES -DSC_USE_PTHREADS 

QUESTAWORK=build/work/
QUESTASCWORK=$(QUESTAWORK)_sc/linux_gcc-4.7.4/
QUESTACC=sccom
QUESTACCFLAGS=-nologo -work $(QUESTAWORK) $(PYTHONFLAGS) $(INCLUDES)

TCLWORK=build/tcl/
TCLCC=g++
TCLCCFLAGS=-Wall $(TCLFLAGS) $(INCLUDES) -Ibuild/.conf_check_deps/dist/systemc-2.3.0/include -Lbuild/.conf_check_deps/dist/systemc-2.3.0/lib -lsystemc -lpthread -ldl -util -lm -ltcl
TCLSWIG=swig -c++ -tcl -Wall -Ipysc -I. -I/usr/include -Ibuild/.conf_check_deps/dist/systemc-2.3.0/include -DLITTLE_ENDIAN_BO -D_REENTRANT -DUSE_STATIC_CASTS -DSC_INCLUDE_DYNAMIC_PROCESSES -DSC_USE_PTHREADS 

#SOURCE=core/common/scireg.cpp pysc/usi/core/registry.cpp pysc/usi/core/api.cpp pysc/usi/core/module.cpp pysc/tests/questasim/tlm2_getting_started_1.cpp pysc/usi/api/systemc.cpp
SOURCE=core/common/scireg.cpp pysc/tests/questasim/tlm2_getting_started_1.cpp pysc/usi/api/systemc.cpp
SWIGIF=pysc/usi/api/systemc.i pysc/usi/api/delegate.i pysc/usi/api/scireg.i


all: questasim tcl
	
questasim: $(patsubst %.cpp, $(QUESTASCWORK)%.o, $(notdir $(SOURCE))) $(patsubst %.i, $(QUESTASCWORK)%.swig.o, $(notdir $(SWIGIF)))
	$(QUESTACC) -link $(QUESTACCFLAGS)

$(addsuffix _info, $(QUESTAWORK)):
	vlib $(QUESTAWORK)

clean:
	-rm -r $(QUESTAWORK)
	-rm -r $(TCLWORK)

define questaswig_obj
$(addprefix $(QUESTAWORK), $(notdir $(1:%.i=%.cpp))): $(1) $(addsuffix _info, $(QUESTAWORK))
	$$(PYSWIG) -o $$@ $$<

$(addprefix $(QUESTASCWORK), $(notdir $(1:%.i=%.swig.o))): $(addprefix $(QUESTAWORK), $(notdir $(1:%.i=%.cpp))) $(addsuffix _info, $(QUESTAWORK))
	$$(QUESTACC) $$(QUESTACCFLAGS) $$<

endef

define questasccom_obj
$(addprefix $(QUESTASCWORK), $(notdir $(1:%.cpp=%.o))): $(1) $(addsuffix _info, $(QUESTAWORK))
	$$(QUESTACC) $$(QUESTACCFLAGS) $$<

endef

$(foreach src, $(SOURCE), $(eval $(call questasccom_obj, $(src))))
$(foreach src, $(SWIGIF), $(eval $(call questaswig_obj, $(src))))


tcl: $(addprefix $(TCLWORK), tclsim)

$(addprefix $(TCLWORK), tclsim): $(patsubst %.cpp, $(TCLWORK)%.o, $(notdir $(SOURCE))) $(patsubst %.i, $(TCLWORK)%.swig.o, $(notdir $(SWIGIF)))
	$(TCLCC) $(TCLCCFLAGS) -o $@ $^

$(addsuffix _info, $(TCLWORK)):
	mkdir -p $(TCLWORK)
	touch $(TCLWORK)_info

define tclswig_obj
$(addprefix $(TCLWORK), $(notdir $(1:%.i=%.cpp))): $(1) $(addsuffix _info, $(TCLWORK))
	$$(TCLSWIG) -o $$@ $$<

$(addprefix $(TCLWORK), $(notdir $(1:%.i=%.swig.o))): $(addprefix $(TCLWORK), $(notdir $(1:%.i=%.cpp))) $(addsuffix _info, $(TCLWORK))
	$$(TCLCC) $$(TCLCCFLAGS) -c -o $$@ $$<

endef

define tclcc_obj
$(addprefix $(TCLWORK), $(notdir $(1:%.cpp=%.o))): $(1) $(addsuffix _info, $(TCLWORK))
	$$(TCLCC) $$(TCLCCFLAGS) -c -o $$@ $$<

endef
$(foreach src, $(SOURCE), $(eval $(call tclcc_obj, $(src))))
$(foreach src, $(SWIGIF), $(eval $(call tclswig_obj, $(src))))
