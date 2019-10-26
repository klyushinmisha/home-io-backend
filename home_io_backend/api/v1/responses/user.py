from . import JsonApiResponse
from ..schemas import UserReadSchema


class UserResponse(JsonApiResponse):
    def __init__(self, user):
        response = UserReadSchema.load(user)
        status = 200
        super().__init__(response, status)


class UserNotFoundResponse(JsonApiResponse):
    def __init__(self):
        response = {
            'errorCode': 'userNotFound'
        }
        status = 404
        super().__init__(response, status)


class UserInvalidPasswordResponse(JsonApiResponse):
    def __init__(self):
        response = {
            'errorCode': 'userInvalidPassword'
        }
        status = 400
        super().__init__(response, status)
