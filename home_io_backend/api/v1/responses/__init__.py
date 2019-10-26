import json

from flask import Response


class JsonApiResponse(Response):
    def __init__(self, response, status):
        super().__init__(
            json.dumps(response),
            status,
            mimetype='application/json'
        )


class JsonApiErrorResponse(Response):
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
