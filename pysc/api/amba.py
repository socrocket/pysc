import pyamba

class AMBADelegate(object):
    def __init__(self, devs):
        self.__devs__ = devs
        super(AMBADelegate, self).__init__()

    def __dir__(self):
        result = set()
        for dev in self.__devs__:
            result.update(dir(dev))
        result.discard('this')
        return sorted(result)

    def __getattr__(self, name):
        result = None
        for dev in self.__devs__:
            result = getattr(dev, name, None)
            if result:
                return result
        super(AMBADelegate, self).__getattr__(name)

def find_amba_device(name):
    return AMBADelegate(pyamba.find_amba_device(name))

