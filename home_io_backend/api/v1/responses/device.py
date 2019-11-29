from ..schemas import DeviceReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse

__all__ = [
    'DeviceResponse',
    'DeviceConnectedResponse',
    'DeviceNotFoundResponse',
    'DeviceAlreadyExistsResponse',
    'DeviceAccessDeniedResponse'
]


class DeviceResponse(JsonApiResponse):
    def __init__(self, device):
        super().__init__(DeviceReadSchema.dump(device), 200)


class DeviceConnectedResponse(JsonApiResponse):
    def __init__(self, access_token):
        super().__init__({
            'access_token': access_token
        }, 200)


class DeviceNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('DEVICE_NOT_FOUND', 404)


class DeviceAlreadyExistsResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('DEVICE_ALREADY_EXISTS', 400)


class DeviceAccessDeniedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('DEVICE_ACCESS_DENIED', 403)
