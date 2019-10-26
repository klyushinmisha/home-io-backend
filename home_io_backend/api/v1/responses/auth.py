from . import JsonApiResponse
from ..schemas import UserReadSchema


class LoginResponse(JsonApiResponse):
    def __init__(self, token):
        response = {
            'access_token': token
        }
        super().__init__(response, 200)
