from __future__ import print_function
import usi
import sys

def load(*k, **kw):
    """Load initial model configuration"""
    from tools.python.arguments import parser
    parser.add_argument('-o', '--option', dest='option', action='append', type=str, help='Give configuration option')
    parser.add_argument('-p', '--python', dest='python', action='append', type=file, help='Execute python scripts')
    parser.add_argument('-j', '--json', dest='json', action='append', type=str, help='Read JSON configuration')
    parser.add_argument('-l', '--list', dest='list', action='store_true', help='List options')

def view(*k, **kw):
    """View detailed model configuration"""
    total = {}
    out_category = {
        "sta_power": "Static power (leakage): %0.4f pW",
        "int_power": "Internal power (dynamic): %0.4f uW",
        "swi_power": "Switching power (dynamic): %0.4f uW"
    }
    params = usi.cci.parameter.readPropertyDict()
    params = usi.cci.parameter.filterDict(params, "power")
    param_list = usi.cci.parameter.paramsToDict(params)
    out = {}
    for base, value in param_list.items():
        parts = base.rsplit(".power.", 1)
        if len(parts) == 2:
          name = parts[0]
          var = parts[1]
          if name not in out:
            out[name] = dict()
          out[name][var] = value
        else:
          print("Mal formated power parameter:", base)

    for comp, var in out.items():
        print("*****************************************************")
        print("* Component:", comp)
        print("* ---------------------------------------------------")
        for name, val in var.items():
            if name in list(out_category.keys()):
                print("*", out_category[name] % val)
                if name not in total:
                  total[name] = 0.0
                total[name] += val
        print ("*****************************************************")
    print ("*****************************************************")
    print ("* Power Summary:")
    print ("* ---------------------------------------------------")
    total_sum = 0.0
    total["sta_power"] /= 10e+6
    for name in list(out_category.keys()):
        print("*", out_category[name] % total[name])
        total_sum += total[name]
    print("* ---------------------------------------------------")
    print("* Total Power: %0.4f" % total_sum, "uW")
    print("*****************************************************")
    #usi.api.parameter.printDict(params)

def install():
    #load()
    usi.on("end_of_evaluation")(view)

if __name__ == "__main__":
    install()

