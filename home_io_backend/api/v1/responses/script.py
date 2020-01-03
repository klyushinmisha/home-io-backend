__all__ = [
    'ScriptResponse',
    'ScriptDeleteResponse',
    'ScriptNotFoundResponse',
    'ScriptAccessDeniedResponse',
    'ScriptBuildStartedResponse',
    'ScriptTagAlreadyExistsResponse',
    'ScriptEnableSwitchedResponse'
]

from ..schemas import ScriptReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse


class ScriptResponse(JsonApiResponse):
    def __init__(self, script, code=None):
        data = ScriptReadSchema.dump(script)
        if code is not None:
            data['code'] = code
        super().__init__(data, 200)


class ScriptDeleteResponse(JsonApiResponse):
    def __init__(self):
        super().__init__('SCRIPT_DELETED', 200)


class ScriptBuildStartedResponse(JsonApiResponse):
    def __init__(self):
        super().__init__('SCRIPT_BUILD_STARTED', 200)


class ScriptEnableSwitchedResponse(JsonApiResponse):
    def __init__(self):
        super().__init__('SCRIPT_ENABLE_SWITCHED', 200)


class ScriptAccessDeniedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('SCRIPT_ACCESS_DENIED', 403)


class ScriptNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('SCRIPT_NOT_FOUND', 404)


class ScriptTagAlreadyExistsResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('SCRIPT_TAG_ALREADY_EXISTS', 404)
