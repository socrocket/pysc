from __future__ import print_function
import re
import pandas as pd
import sys
import os


# read Modelsim/Questa logfile
def read_log(filename):
    log_re = re.compile("\A#")
    message_re = re.compile("\A#\s+(\d+)\s+([a-z]+)\s+:\s+(\S+):\s+(0x[0-9a-f]+)\s+(.*)")
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
                        'component_name': result.group(3),
                        'pc': int(result.group(4), 16),
                        'message': result.group(5)}
                message = result.group(5)
                data['time'] = data['time'] * time_unit_factor(data['time_unit'])
                data['time_unit'] = "ps"
                data['index_p'] = index
                data_aggr.append(data)
                index += 1
                if index % 25000 == 0:
                    store.append('log', pd.DataFrame(data_aggr), min_itemsize = 50, data_columns=list(data.keys()))
                    data_aggr = []
    if len(data_aggr) > 0:
        store.append('log', pd.DataFrame(data_aggr), min_itemsize = 50)

    store.close()

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
        print("Usage: python transcript2db <log_file>")
        print("The database will be stored as <log_file>.h5")
    else:
        filename = sys.argv[1]
        read_log(filename)
