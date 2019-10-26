import json

from flask import Response


class JsonApiResponse(Response):
    def __init__(self, response, status):
        super().__init__(
            json.dumps(response),
            status,
            mimetype='application/json'
        )


class JsonMimetypeRequiredResponse(JsonApiResponse):
    def __init__(self):
        response = {
            'errorCode': 'jsonMimetypeRequired'
        }
        status = 400
        super().__init__(response, status)


class MimetypeValidationError(JsonApiResponse):
    def __init__(self):
        response = {
            'errorCode': 'mimetypeValidationError'
        }
        status = 400
        super().__init__(response, status)


class JsonValidationErrorResponse(JsonApiResponse):
    def __init__(self):
        response = {
            'errorCode': 'jsonValidationError'
        }
        status = 400
        super().__init__(response, status)
