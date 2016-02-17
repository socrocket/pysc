from __future__ import print_function
import usi
from usi import shell
from sr_register import scireg

def implements_scireg(component):
    return 'scireg_get_region_type' in dir(component)

@usi.on('start_of_simulation')
def onstart(*k, **kw):
    banks = []
    search_result = usi.find('leon3_0.dvectorcache.line_63.*')
    for component in search_result:
        if implements_scireg(component) and\
           component.scireg_get_region_type() == scireg.SCIREG_BANK:
                banks.append(component)

    total_bytes_banks = 0
    for bank in banks:
        print(bank.name())
        #for bank in bank.scireg_get_child_regions():
        #    print(bank)

        #total_bytes_banks += bank.scireg_get_byte_width()
        #print(bank.scireg_get_byte_width())
    #print('Total bytes in banks: {}; {} MB'.format(total_bytes_banks, total_bytes_banks / (1024 * 1024)))

    #shell.start()
