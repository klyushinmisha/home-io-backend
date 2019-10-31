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
        super().__init__('JSON_MIMETYPE_REQUIRED', 400)


class JsonValidationErrorResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('JSON_VALIDATION_ERROR', 400)


class MimetypeValidationErrorResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('MIMETYPE_VALIDATION_ERROR', 400)


class BadRequestResponse(JsonApiErrorResponse):
    def __init__(self, body):
        super().__init__('BAD_REQUEST', 400, body=body)


class NotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('NOT_FOUND', 404)


class MethodNotAllowedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('METHOD_NOT_ALLOWED', 405)


class InvalidBodyResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('INVALID_BODY_ERROR', 422)
