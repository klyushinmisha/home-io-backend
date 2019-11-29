__all__ = [
    'ScriptResponse',
    'ScriptDeleteResponse',
    'ScriptNotFoundResponse',
    'ScriptAccessDeniedResponse',
    'ScriptBuildStartedResponse',
    'ScriptTagAlreadyExistsResponse'
]

from ..schemas import ScriptReadSchema
from ...common.responses import JsonApiResponse, JsonApiErrorResponse


class ScriptResponse(JsonApiResponse):
    def __init__(self, script):
        super().__init__(ScriptReadSchema.dump(script), 200)


class ScriptDeleteResponse(JsonApiResponse):
    def __init__(self):
        super().__init__('', 200)


class ScriptBuildStartedResponse(JsonApiResponse):
    def __init__(self):
        super().__init__('', 200)


class ScriptAccessDeniedResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('SCRIPT_ACCESS_DENIED', 403)


class ScriptNotFoundResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('SCRIPT_NOT_FOUND', 404)


class ScriptTagAlreadyExistsResponse(JsonApiErrorResponse):
    def __init__(self):
        super().__init__('SCRIPT_TAG_ALREADY_EXISTS', 404)
