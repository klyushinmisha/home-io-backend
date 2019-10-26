from . import JsonApiErrorResponse, JsonApiErrorResponse


class JsonMimetypeRequiredResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('jsonMimetypeRequired', 400)


class MimetypeValidationError(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('mimetypeValidationError', 400)


class JsonValidationErrorResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('jsonValidationError', 400)


class InvalidBodyErrorResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('invalidBodyError', 422)


class MethodNotAllowedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('methodNotAllowed', 405)