from flask import request

class ViewException(Exception):
    pass

def init(app, urls):
    for url in urls:
        split = url[1].split('.')
        name_func =  split.pop()
        module = '.'.join(split)
        api = __import__('api.%s' % module)
        try:
            func = getattr(getattr(api, module), name_func)
        except Exception, e:
            raise ViewException('The view "%s" does not have the "%s" method' % (module, name_func))
        try:
            app.route(url[0], methods=url[2])(func)
        except Exception, e:
            raise ViewException(e)
