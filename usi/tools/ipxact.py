from __future__ import print_function
from builtins import object
import pprint
import re
import usi
import sr_registry as registry
from usi import cci
import xml.etree.ElementTree as ET

class IP_XACT(object):
    def __init__(self, filename):
        self.namespaces = {'ipxact': 'http://www.accellera.org/XMLSchema/IPXACT/1685-2014'}
        self.root = ET.parse(filename)

    def get_instances(self):
        result = []
        for instance in self.root.findall('./ipxact:componentInstances/ipxact:componentInstance', self.namespaces):
            parameter =[]
            for config_value in instance.findall('./ipxact:componentRef/ipxact:configurableElementValues/ipxact:configurableElementValue', self.namespaces):
                parameter.append({
                    'name' : config_value.attrib['referenceId'],
                    'value': self._convert_type(config_value.text),
                })
            instance_data = {
                'name'      : instance.find('ipxact:instanceName', self.namespaces).text,
                'reference' : instance.find('ipxact:componentRef', self.namespaces).attrib,
                'parameter' : parameter,
            }
            result.append(instance_data)

        return result

    def get_interconnects(self):
        result = []
        for interconnect in self.root.findall('./ipxact:interconnections/ipxact:interconnection', self.namespaces):
            interfaces = []
            for interface in interconnect.findall('ipxact:activeInterface', self.namespaces):
                interfaces.append(interface.attrib)
            interconnect_data = {
                'name' : interconnect.find('ipxact:name', self.namespaces).text,
                'activeInterfaces' : interfaces,
            }
            result.append(interconnect_data)
        return result

    def _convert_type(self, value):
        print(value)
        if value is None:
            result = None
        elif re.match('^\d+$', value) is not None:
            result = int(value)
        elif re.match('^0x[\da-fA-F]+$', value) is not None:
            result = int(value, 16)
        elif re.match('^true$', value, flags=re.IGNORECASE):
            result = True
        elif re.match('^false$', value, flags=re.IGNORECASE):
            result = False
        else:
            result = value
        return result


if __name__ == "__main__":
    model = IP_XACT('ip-xact.xml')
    pprint.pprint(model.get_instances())
    pprint.pprint(model.get_interconnects())

