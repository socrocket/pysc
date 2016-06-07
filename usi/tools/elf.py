from __future__ import print_function
import usi
import sys
import re
from usi.tools.args import parser, get_args
from elftools.elf.elffile import ELFFile
from elftools.elf import constants
from usi.api import intrinsics
import sr_registry as registry

memoryre = re.compile(r"^(?P<object>[a-zA-Z0-9_.]+)=(?P<filename>[a-zA-Z0-9_\-./]+)(\((?P<baseaddr>\d+|0x\d+)\))?$", re.U)
intrinsicre = re.compile(r"^(?P<object>[a-zA-Z0-9_.]+)=(?P<filename>[a-zA-Z0-9_\-./]+)(\((?P<intrinsics>[a-zA-Z0-9_.,=]+)\))?$", re.U)
intrinsic_groups = {
    'standard': {
      '_exit': '_exitIntrinsic32',
      'chmod': 'chmodIntrinsic32',
      'chown': 'chownIntrinsic32',
      'close': 'closeIntrinsic32',
      'creat': 'creatIntrinsic32',
      'dup2': 'dup2Intrinsic32',
      'dub': 'dupIntrinsic32',
      'error': 'errorIntrinsic32',
      'fstat': 'fstatIntrinsic32',
      'getpid': 'getpidIntrinsic32',
      'gettimeofday': 'gettimeofdayIntrinsic32',
      'isatty': 'isattyIntrinsic32',
      'kill': 'killIntrinsic32',
      'lseek': 'lseekIntrinsic32',
      'lstat': 'lstatIntrinsic32',
      'main': 'mainIntrinsic32',
      'open': 'openIntrinsic32',
      'random': 'randomIntrinsic32',
      'read': 'readIntrinsic32',
      'rename' : 'renameIntrinsic32',
#      'sbrk': 'sbrkIntrinsic32',
      'stat': 'statIntrinsic32',
      'time': 'timeIntrinsic32',
      'times': 'timesIntrinsic32',
      'unlink': 'unlinkIntrinsic32',
      'usleep': 'usleepIntrinsic32',
      'utimes': 'utimesIntrinsic32',
      'write': 'writeIntrinsic32'
    }
}
parser.add_argument('-e', '--loadelf', dest='loadelf', action='append', default=[], type=str, help='Load Data from ELF file into memory')
parser.add_argument('-i', '--intrinsics', dest='intrinsics', action='append', default=[], type=str, help='Load intrinsics for an elf file to a processor')

def load_elf_into_scireg(filename, stores, base):
    with open(filename, "rb") as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if section.header["sh_flags"] & constants.SH_FLAGS.SHF_ALLOC:
                addr = section.header["sh_addr"] - base
                data = section.data()

                if isinstance(stores, usi.USIDelegate):
                    stores = [stores]
                for store in stores:
                    if isinstance(store, str):
                        store = store.encode('utf-8')
                    print("Loading %s into %s at address %s" % (filename, store.name(), base))
                    if sys.version_info >= (3,0):
                        store.scireg_write(data, int(addr))
                    else:
                        store.scireg_write(data, long(addr))

def load_elf_intrinsics_to_processor(filename, cpus, intrinsics):
    with open(filename, "rb") as stream:
        elf = ELFFile(stream)
        for section in elf.iter_sections():
            if section.header['sh_type'] == 'SHT_SYMTAB':
                for name, klass, entry in [(name, intrinsics[name], entry) for name, entry in [(symbol.name.decode('utf-8'), symbol.entry) for symbol in section.iter_symbols()] if name in list(intrinsics.keys())]:
                    for cpu in cpus:
                        intrinsic_manager = None
                        if 'register_intrinsic' in dir(cpu):
                            intrinsic_manager = cpu
                        else:
                            for child in cpu.children():
                                if child.basename() == 'intrinsics' and 'register_intrinsic' in dir(child):
                                    intrinsic_manager = child
                                    break

                        if not intrinsic_manager:
                            print("intrinsic manager for cpu %s not found" % cpu.name())
                        print("Intrinsic on symbol %s at address %x is inserted with class %s on CPU %s" % (name, entry['st_value'], klass, cpu.name()))
                        intrinsic_instance = registry.api.create_object_by_name('PlatformIntrinsic', klass, str(name))
                        intrinsic_manager.register_intrinsic(entry['st_value'], intrinsic_instance)

@usi.on('start_of_simulation')
def start_of_simulation(*k, **kw):
    for param in get_args().loadelf:
        result = memoryre.match(param)
        if not result:
            print("-e takes always a key/value pair. '%s' is not a key/value pair. The value must be contain a file name and a base address: '-e sdram=hello.sparc(0x40000000)'" % (param))
            continue
        groups = result.groupdict()
        if not 'object' in groups or not 'filename' in groups:
            print("-e takes always a key/value pair. '%s' is not a key/value pair. The value must be contain a file name and a base address: '-e sdram=hello.sparc(0x40000000)'" % (param))
            continue
        obj = groups['object']
        filename = groups['filename']
        if "baseaddr" in groups and groups['baseaddr']:
            base = int(groups['baseaddr'], 0) # not 100% right, won't work in the case when there is no 0x in front of Hex string!
        elif filename.endswith('.sparc') or filename.endswith('.dsu'):
            base = 0x40000000
        else:
            base = 0x00000000
        stores = usi.find(obj)
        if len(stores) == 0:
            print("scireg %s not found in simulation for parameter -e %s" % (obj, param))
            continue

        load_elf_into_scireg(filename, stores, base)

    for param in get_args().intrinsics:
        result = intrinsicre.match(param)
        if not result:
            print("-i takes always a key/value pair. '%s' is not a key/value pair. The value must be contain a file name and a list of intrinsics: '-i leon3_0=hello.sparc(open,close)'" % (param))
            continue
        groups = result.groupdict()
        if not 'object' in groups or not 'filename' in groups or not 'intrinsics':
            print("-i takes always a key/value pair. '%s' is not a key/value pair. The value must be contain a file name and a base address: '-i leon3_0=hello.sparc(open,close)'" % (param))
            continue
        obj = groups['object']
        filename = groups['filename']
        intrinsiclist = groups['intrinsics'].split(',')
        intrinsics = {}
        for intrinsic in intrinsiclist:
            splitted = intrinsic.split('=')
            if len(splitted) == 1:
                if splitted[0] in intrinsic_groups:
                    intrinsics.update(intrinsic_groups[splitted[0]])
                else:
                    intrinsics[splitted[0]] = splitted[0]

            elif len(splitted) > 1:
                if splitted[1] == 'None':
                    del(intrinsics[splitted[0]])
                else:
                    intrinsics[splitted[0]] = splitted[1]
            else:
                pass
        cpus = usi.find(obj)
        if len(cpus) == 0:
            print("cpu %s not found in simulation for parameter -i %s" % (obj, param))
            continue

        load_elf_intrinsics_to_processor(filename, cpus, intrinsics)
