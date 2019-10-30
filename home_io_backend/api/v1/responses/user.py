from ..schemas import UserReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse

__all__ = [
    'UserResponse',
    'UserNotFoundResponse',
    'UserInvalidPasswordResponse',
    'UsernameAlreadyExistResponse',
    'EmailAlreadyExistResponse',
]


class UserResponse(JsonApiResponse):
    def __init__(self, user):
        super().__init__(UserReadSchema.dump(user), 200)


class UserNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('userNotFound', 404)


class UserInvalidPasswordResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('userInvalidPassword', 400)


class UsernameAlreadyExistResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('usernameAlreadyExist', 400)



class EmailAlreadyExistResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('emailAlreadyExist', 400)
