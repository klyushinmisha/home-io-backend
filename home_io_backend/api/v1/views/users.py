from webargs.flaskparser import use_kwargs


from .. import api
from ..responses.user import *
from ..schemas import UserCreateSchema
from ..view_decorators import json_mimetype_required
from ....models import User, db


@api.route('/users', methods=['POST'])
@use_kwargs(UserCreateSchema, locations=('json',))
def create_new_user(email, username, password):
    check_user = User.query.filter(
        User.username == username
    ).one_or_none()
    if check_user is not None:
        return UserAlreadyExistResponse()
    user = User(
        email=email,
        username=username,
        password=password,
    )
    db.session.add(user)
    db.session.commit()
    return UserResponse(user)


@api.route('/users/<int:id>', methods=['GET'])
@json_mimetype_required
def get_user(id):
    user = User.query.filter(
        User.id == id
    ).one_or_none()
    if user is None:
        UserNotFoundResponse()
    return UserResponse(user)


# @api.route('/users/<int:id>', methods=['PATCH'])
# @json_mimetype_required
# @use_kwargs(UserCreateSchema,locations=('json',))
# def update_user(id):
#     pass