'''This module contains common JSON responses.'''

import json

from flask import Response

__all__ = [
    'JsonApiResponse',
    'JsonApiErrorResponse',
    'JsonMimetypeRequiredResponse',
    'BadRequestResponse',
    'JsonValidationErrorResponse',
    'InvalidBodyResponse',
    'MethodNotAllowedResponse',
    'NotFoundResponse',
]


class JsonApiResponse(Response):
    '''Custom JSON response.
    This is a base class for other API responses.'''
    def __init__(self, response, status):
        super().__init__(
            json.dumps(response),
            status,
            mimetype='application/json'
        )


class JsonApiErrorResponse(Response):
    '''Custom JSON error response.
    This is a base class for other API responses.'''
    def __init__(self, error_code, status, body=None):
        response = {
            'error_code': error_code
        }
        if body is not None:
            response['data'] = body
        super().__init__(
            json.dumps(response),
            status,
            mimetype='application/json'
        )


class JsonMimetypeRequiredResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('jsonMimetypeRequired', 400)


class JsonValidationErrorResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('jsonValidationError', 400)


class MimetypeValidationErrorResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('mimetypeValidationError', 400)


class BadRequestResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('badRequestError', 400)


class NotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('notFoundResponse', 404)


class MethodNotAllowedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('methodNotAllowed', 405)


class InvalidBodyResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('invalidBodyError', 422)
