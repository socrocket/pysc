import usi
from sr_register import scireg
import sys
import re

def convert2int(characters):
    i = 0
    result = 0L
    for char in characters:
        result += (ord(char) << (len(characters)-i)*8)
        i += 1
    return result

@usi.on('start_of_simulation')
def simulation_begin(*k, **kw):

    def read_access(*k, **kw):
        width = k[2].scireg_get_byte_width()
        tag_name = k[2].scireg_get_string_attribute(scireg.SCIREG_NAME)[:-5] + 'tag.atag'
        tag = usi.USIDelegate(tag_name)
        print("Callback: Read access at address {:02} with length of {:02} bytes on {}: current value {:#0{length}x}, with tag {:#08x}"\
                .format(
                    k[0],
                    k[1],
                    k[2].scireg_get_string_attribute(scireg.SCIREG_NAME),
                    convert2int(k[2].scireg_read(long(width))),
                    convert2int(tag.scireg_read(long(4))),
                    length=width*2,
                    )
                )
    
    def write_access(*k, **kw):
        width = k[2].scireg_get_byte_width()
        tag_name = k[2].scireg_get_string_attribute(scireg.SCIREG_NAME)[:-5] + 'tag.atag'
        tag = usi.USIDelegate(tag_name)
        print("Callback: Write access at address {:02} with length of {:02} bytes on {}: current value {:#0{length}x}, with tag {:#08x}"\
                .format(
                    k[0],
                    k[1],
                    k[2].scireg_get_string_attribute(scireg.SCIREG_NAME),
                    convert2int(k[2].scireg_read(long(width))),
                    convert2int(tag.scireg_read(long(4))),
                    length=width*2,
                    )
                )
    
    everything = usi.find('*')
    cache_lines = []
    
    for scobject in everything:
        if re.search(r"leon3_0\.dvectorcache\.line_\d+\.entry", scobject.name()):
            cache_lines.append(scobject)

    for cache_line in cache_lines:
        cache_line.scireg_add_callback((read_access, scireg.SCIREG_READ_ACCESS, long(0), long(4)))
        cache_line.scireg_add_callback((write_access, scireg.SCIREG_WRITE_ACCESS, long(0), long(4)))
