import usi
from sr_register import scireg
import sys
import re

def convert2int(characters):
    i = 0
    result = 0
    for char in characters:
        result += ord(char) << (i*8)
    return result

@usi.on('start_of_simulation')
def simulation_begin(*k, **kw):

    def read_access(*k, **kw):
        print("Callback: Read access at address {} with length of {} bytes on {}: current value {}"\
                .format(k[0], k[1], k[2].scireg_get_string_attribute(scireg.SCIREG_NAME), convert2int(k[2].scireg_read(long(4)))))
    
    def write_access(*k, **kw):
        print("Callback: Write access at address {} with length of {} bytes on {}: current value {}"\
                .format(k[0], k[1], k[2].scireg_get_string_attribute(scireg.SCIREG_NAME), convert2int(k[2].scireg_read(long(4)))))
    
    everything = usi.find('*')
    cache_lines = []
    
    for scobject in everything:
        if re.search(r"leon3_0\.ivectorcache\.line_\d+\.tag\.valid", scobject.name()):
            cache_lines.append(scobject)

    for cache_line in cache_lines:
        cache_line.scireg_add_callback((read_access, scireg.SCIREG_READ_ACCESS, long(0), long(4)))
        cache_line.scireg_add_callback((write_access, scireg.SCIREG_WRITE_ACCESS, long(0), long(4)))
