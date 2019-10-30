from webargs.flaskparser import FlaskParser

from ...common.responses import BadRequestResponse

parser = FlaskParser()

from marshmallow.exceptions import MarshmallowError

@parser.error_handler
def handle_error(error, req, schema, status_code, headers):
    raise MarshmallowError(error)

from .auth import *
from .users import *
