from __future__ import print_function
import re
import pandas as pd
import sys
import os


# read SoCRocket logfile
def read_log(filename):
    log_re = re.compile("\A@")
    message_re = re.compile("\A@(\d+)\s+([a-z]+)\s+/(\d+)\s+\((\S+)\):\s+(\S+):\s+(.*)")
    ansi_escape_re = re.compile(r'\x1b[^m]*m')

    file = open(filename)

    h5_path = filename+".h5"
    if os.path.exists(h5_path):
        os.remove(h5_path)

    store = pd.HDFStore(h5_path)
    index = 0

    data_aggr = []

    for line in file:
        if log_re.match(line):
            pure_line = ansi_escape_re.sub('', line)
            result = message_re.match(pure_line)
            if result:
                data = {'time': int(result.group(1)),
                        'time_unit': result.group(2),
                        'delta_cycle': int(result.group(3)),
                        'component_name': result.group(4)}
                log_level = result.group(5)
                message = result.group(6)
                if log_level == 'Analysis':
                    data['time'] = data['time'] * time_unit_factor(data['time_unit'])
                    data['time_unit'] = "ps"
                    data['index_p'] = index
                    data = dict(data.items() + list(parse_message(message).items()))
                    data_aggr.append(data)
                    index += 1
                    if index % 25000 == 0:
                        store.append('log', pd.DataFrame(data_aggr), min_itemsize = 30, index=False, data_columns=True)
                        data_aggr = []
    if len(data_aggr) > 0:
        store.append('log', pd.DataFrame(data_aggr), min_itemsize = 30, index=False, data_columns=True)
    store.create_table_index('log', kind='full')
    store.close()

def parse_message(message):
    result = {}
    variables = message.split()
    sep_re = re.compile("(.*)=(.*)")
    dec_re = re.compile("\A\d+\Z")
    hex_re = re.compile("\A0x[0-9a-fA-F]+\Z")
    for variable in variables:
        separate = re.match("(.*)=(.*)", variable)
        if separate:
            key = separate.group(1)
            value = separate.group(2)
            if dec_re.match(value):
                value = int(value)
            elif hex_re.match(value):
                value = int(value, 16)
            result[key] = value
    return result

# get normalised time
def time_unit_factor(unit):
    if unit == "s":
        return 1000000000000
    elif unit == "ms":
        return 1000000000
    elif unit == "us":
        return 1000000
    elif unit == "ns":
        return 1000
    elif unit == "ps":
        return 1
    else:
        raise Exeption("Unknown time unit!")
    return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: log2db.py <log_file>")
        print("Database will be stored as <log_file>.h5")
    else:
        filename = sys.argv[1]
        read_log(filename)
