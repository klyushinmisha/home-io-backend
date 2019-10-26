from . import JsonApiResponse


class LoginResponse(JsonApiResponse):
    def __init__(self, token):
        response = {
            'accessToken': token
        }
        status = 200
        super().__init__(response, status)
