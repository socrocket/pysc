from __future__ import print_function
import usi
from usi import shell
from sr_register import scireg

def implements_scireg(component):
    return 'scireg_get_region_type' in dir(component)

@usi.on('start_of_simulation')
def onstart(*k, **kw):
    registers = []
    search_result = usi.find('*')
    for component in search_result:
        if implements_scireg(component) and\
           component.scireg_get_region_type() == scireg.SCIREG_REGISTER:
                registers.append(component)

    total_bytes_register = 0
    for register in registers:
        print(register.name())
        total_bytes_register += register.scireg_get_byte_width()
    print('Total bytes in registers: {}'.format(total_bytes_register))
    
    #shell.start()
