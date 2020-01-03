from ..schemas import DeviceReadSchema, DeviceTasksReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse

__all__ = [
    'DeviceResponse',
    'DeviceConnectedResponse',
    'DeviceNotFoundResponse',
    'DeviceAlreadyExistsResponse',
    'DeviceAccessDeniedResponse',
    'DeviceTasksResponse',
    'DeviceScriptsStartedResponse',
    'DeviceLogsResponse',
    'DeviceTaskCreatedResponse'
]


class DeviceResponse(JsonApiResponse):
    def __init__(self, device):
        super().__init__(DeviceReadSchema.dump(device), 200)


class DeviceScriptsStartedResponse(JsonApiResponse):
    def __init__(self):
        super().__init__('DEVICE_SCRIPTS_STARTED', 200)


class DeviceTasksResponse(JsonApiResponse):
    def __init__(self, tasks):
        super().__init__(DeviceTasksReadSchema.dump(tasks), 200)


class DeviceConnectedResponse(JsonApiResponse):
    def __init__(self, access_token):
        super().__init__({
            'access_token': access_token
        }, 200)


class DeviceLogsResponse(JsonApiResponse):
    def __init__(self, logs):
        super().__init__({
            'logs': logs
        }, 200)


class DeviceTaskCreatedResponse(JsonApiResponse):
    def __init__(self):
        super().__init__('TASK_CREATED_RESPONSE', 200)


class DeviceNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('DEVICE_NOT_FOUND', 404)


class DeviceAlreadyExistsResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('DEVICE_ALREADY_EXISTS', 400)


class DeviceAccessDeniedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('DEVICE_ACCESS_DENIED', 403)
