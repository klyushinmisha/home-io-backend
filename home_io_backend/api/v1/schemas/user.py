from marshmallow import fields, validate, Schema
from marshmallow.exceptions import ValidationError
from marshmallow_arrow import ArrowField
from sqlalchemy.orm.exc import MultipleResultsFound

from ....models import User


class UserSchema(Schema):

    model = User

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
        exclude=('owner_id', ),
        many=True
    )
