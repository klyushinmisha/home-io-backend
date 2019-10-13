__all__ = [
    'UserReadSchema',
    'UsersReadSchema',
    'UserCreateSchema',
    'UserUpdateSchema'
]

from marshmallow import fields, validate, Schema
from marshmallow_arrow import ArrowField


class UserSchema(Schema):
    id = fields.Integer()

    username = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=32),
            validate.Regexp(r"[\w]+")
        ]
    )

    email = fields.Email(
        required=True,
        validate=[
            validate.Length(min=8, max=64),
            validate.Regexp(r"[\w@]+")
        ]
    )

    password = fields.String(
        required=True,
        validate=[
            validate.Length(min=8, max=32),
            validate.Regexp(r"[\w]+")
        ]
    )

    created_at = ArrowField()

    devices = fields.Nested(
        'DeviceSchema',
        exclude=('user', ),
        many=True
    )


UserReadSchema = UserSchema()
UsersReadSchema = UserSchema(many=True)
UserCreateSchema = UserSchema(
    exclude=('id', 'created_at', 'devices')
)
UserUpdateSchema = UserSchema(
    exclude=('id', 'created_at', 'devices'),
    partial=True
)
