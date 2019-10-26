import functools

from flask import request
from webargs import flaskparser

from ..responses import JsonMimetypeRequiredResponse, \
    MimetypeValidationError, JsonValidationErrorResponse


def json_mimetype_required(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return JsonMimetypeRequiredResponse()
        return view(*args, **kwargs)
    return wrapper


def mimetype_required(*mimetypes):
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            if request.mimetype not in mimetypes:
                raise MimetypeValidationError(*mimetypes)
            return view(*args, **kwargs)
        return wrapper
    return decorator


parser = flaskparser.FlaskParser()


def use_args(*args, **kwargs):
    def decorator(view):
        @functools.wraps(view)
        def wrapper(*args, **kwargs):
            try:
                parser.parse(locations=('query', ))
            except:
                return JsonValidationErrorResponse()
            return view(*args, **kwargs)
        return wrapper
    return decorator


from .auth import *
