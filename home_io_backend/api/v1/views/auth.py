__all__ = [
    'login'
]

from flask_jwt_extended import create_access_token
from sqlalchemy.orm.exc import MultipleResultsFound
from webargs.flaskparser import use_kwargs

from ..responses.auth import LoginResponse
from ..responses.user import UserNotFoundResponse, \
    UserInvalidPasswordResponse
from . import json_mimetype_required
from .. import api
from ..schemas.auth import LoginSchema
from ....models import User


@api.route('/login', methods=['POST'])
@json_mimetype_required
@use_kwargs(LoginSchema(), locations=("json",))
def login(username, password):
    user = User.query.filter(
        User.username == username
    ).one_or_none()
    if user is None:
        return UserNotFoundResponse()
    if user.check_password(password):
        access_token = create_access_token(identity=username)
        return LoginResponse(access_token)
    else:
        return UserInvalidPasswordResponse()
