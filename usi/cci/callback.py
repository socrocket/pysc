from usi.api import cci as api

pre_read = api.pre_read
post_read = api.post_read
reject_write = api.reject_write
pre_write = api.pre_write
post_write = api.post_write
create_param = api.create_param
destroy_param = api.destroy_param
post_write_and_destroy = api.post_write_and_destroy
no_callback = api.no_callback

register = api.register_callback
unregister = api.unregister_callback

def on(name, type):
    def do(funct):
        return register(name, funct, type)
    return do

