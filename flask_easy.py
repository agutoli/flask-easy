import sys
from flask import current_app, request, Response as FlaskResponse, abort

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

class HttpResponse(object):

    status=None
    headers=None
    content_type=None
    direct_passthrough=None
    
    def type(self, mimetype, **typekwargs):

        # reset instance
        instance = object.__new__(HttpResponse)
        self.__dict__= instance.__dict__

        for arg in typekwargs:
            setattr(instance, arg, typekwargs[arg])

        def wrapper(func):
            attr_name = ''
            for item in func.func_globals:
                if isinstance(func.func_globals[item], HttpResponse):
                    attr_name = item
            def Proxy(*args, **kwargs):
                func.func_globals[attr_name] = instance
                res = func(*args, **kwargs)
                return FlaskResponse(response=res, mimetype=mimetype, 
                        status=instance.status, headers=instance.headers, 
                        content_type=instance.content_type, 
                        direct_passthrough=instance.direct_passthrough)
            Proxy.__name__ = func.__name__
            return Proxy
        return wrapper

class HttpRequest(object):
    def allowed_args(self, dict_args):
        parsed_args = {}
        for arg in request.args.items():
            arg_name = arg[0]
            arg_value = arg[1]

            # defaults keys
            new_dict = dict({
                "default": None,
                "type": None,
                "required": False,
                "max": None,
                "min": None
            }.items() + dict_args[arg_name].items())

            # invalid args
            if not arg_name in dict_args:
                abort(400, "Invalid parameter '%s' not allowed" % arg_name)

            try:
                parsed_args[arg_name] = new_dict['type'](arg_value)
            except ValueError, e:
                abort(400, "Parameter '%s' must be '%s' and not '%s'" % (arg_name, 
                    new_dict['type'].__name__, type(arg_value).__name__))

            if type(parsed_args[arg_name]) in (int, float, long):
                if parsed_args[arg_name] > new_dict['max'] and new_dict['max'] != None:
                    abort(400, "Parameter '%s' must be less than or equal to '%s'" % (arg_name, new_dict['max']))

                if parsed_args[arg_name] < new_dict['min'] and new_dict['min'] != None:
                    abort(400, "Parameter '%s' must be greater than or equal to '%s'" % (arg_name, new_dict['min']))
            else:
                if new_dict['max'] != None:
                    abort(500, "Param '%s' is '%s' type and can not be used with 'max'" % (arg_name, new_dict['type'].__name__))

                if new_dict['min'] != None:
                    abort(500, "Param '%s' is '%s' type and can not be used with 'min'" % (arg_name, new_dict['type'].__name__))


        return parsed_args 
    
Request = HttpRequest()
Response = HttpResponse()




