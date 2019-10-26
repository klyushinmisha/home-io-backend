import functools
from ...v1 import api

from flask import request
from webargs import flaskparser
from marshmallow.exceptions import ValidationError

from ..responses.common import JsonMimetypeRequiredResponse,\
    MimetypeValidationError, JsonValidationErrorResponse,\
    InvalidBodyErrorResponse, MethodNotAllowedResponse


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


@api.errorhandler(422)
def handle_unprocessible(error):
    return InvalidBodyErrorResponse()


from .auth import *
