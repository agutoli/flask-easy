import sys
from flask import current_app, Response as FlaskResponse

# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

class ViewException(Exception):
    pass

class Easy(object):

    def __init__(self, app):
        self._app = app

    def _apply_url_rule(self, rule, view_func, options):
        try:
            self._app.route(rule, methods=options)(view_func)
        except Exception, e:
            raise ViewException(e)

    def _get_view_func(self, mod_name, func_name):
        try:
            return getattr(sys.modules[mod_name], func_name)
        except Exception, e:
            raise ViewException('The view "%s" does not have the "%s" method' % (mod_name, name_func))

    def add_url_rules(self, rules):
        for rule in rules:
            split = rule[1].split('.')
            name_func =  split.pop()
            mod_name = '.'.join(split)
            module = __import__(mod_name)
            # return view func
            view_func = self._get_view_func(mod_name, name_func)
            # apply url's rule
            self._apply_url_rule(rule[0], view_func, rule[2])

class Response(object):
    def type(self, _type):
        def wrapper(func):
            def Proxy():
                return FlaskResponse(response=func(), mimetype=_type)
            Proxy.__name__ = func.__name__
            return Proxy
        return wrapper

Response = Response()




