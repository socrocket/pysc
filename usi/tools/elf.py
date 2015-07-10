import usi
import sys
from usi.tools.args import parser, get_args

parser.add_argument('-e', '--loadelf', dest='loadelf', action='append', default=[], type=str, help='Load Data from ELF file into memory')

@usi.on('start_of_simulation')
def start_of_initialization(*k, **kw):
    from elftools.elf.elffile import ELFFile
    from elftools.elf import constants
    for param in get_args().loadelf:
        paramlist = param.split('=')
        if len(paramlist) != 2:
            print "-e takes always a key/value pair. '%s' is not a key/value pair. The value must be contain a file name and a base address: '-e sdram=hello.sparc(0x40000000)'" % (param)
        obj = paramlist[0]
        paramlist2 = paramlist[1].split('(')
        if len(paramlist2) > 2:
            print "-e takes always a key/value pair. '%s' is not a key/value pair. The value must be contain a file name and a base address: '-e sdram=hello.sparc(0x40000000)'" % (param)
        filename = paramlist2[0]
        if len(paramlist2) == 2:
            base = int(paramlist2[1].strip(')'), 0) # not 100% right, won't work in the case when there is no 0x in front of Hex string!
        elif filename.endswith('.sparc'):
            base = 0x40000000
        else:
            base = 0x00000000
        stores = usi.find(obj)
        if len(stores) == 0:
            print "scireg %s not found in simulation for parameter -e %s" % (obj, param)

        print "Loading %s into %s at address %s" % (filename, obj, base)
        with open(filename, "rb") as stream:
            elf = ELFFile(stream)
            for section in elf.iter_sections():
                if section.header["sh_flags"] & constants.SH_FLAGS.SHF_ALLOC:
                    addr = section.header["sh_addr"] - base
                    data = section.data()
                    
                    for store in stores:
                        store.scireg_write(data, addr)
