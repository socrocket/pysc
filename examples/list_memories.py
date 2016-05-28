from __future__ import print_function
import usi
from usi import shell
from sr_register import scireg

def implements_scireg(component):
    return 'scireg_get_region_type' in dir(component)

@usi.on('start_of_simulation')
def onstart(*k, **kw):
    memories = []
    search_result = usi.find('*')
    for component in search_result:
        if implements_scireg(component) and\
           component.scireg_get_region_type() == scireg.SCIREG_MEMORY:
                memories.append(component)

    total_bytes_memories = 0
    for memory in memories:
        print(memory.name())
        total_bytes_memories += memory.scireg_get_byte_width()
        print(memory.scireg_get_byte_width())
    print('Total bytes in memories: {}; {} MB'.format(total_bytes_memories, total_bytes_memories / (1024 * 1024)))

    #shell.start()
