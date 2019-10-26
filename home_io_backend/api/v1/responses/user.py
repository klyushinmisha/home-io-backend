from . import JsonApiResponse, JsonApiErrorResponse
from ..schemas import UserReadSchema


class UserResponse(JsonApiResponse):
    def __init__(self, user):
        super().__init__(UserReadSchema.load(user), 200)


class UserNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('userNotFound', 404)


class UserInvalidPasswordResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('userInvalidPassword', 400)
