from ..schemas import UserReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse

__all__ = [
    'UserResponse',
    'UserNotFoundResponse',
    'UserInvalidPasswordResponse',
]


class UserResponse(JsonApiResponse):
    def __init__(self, user):
        super().__init__(UserReadSchema.load(user), 200)


class UserNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('userNotFound', 404)


class UserInvalidPasswordResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('userInvalidPassword', 400)
