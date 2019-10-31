from marshmallow import fields, validate, Schema
from marshmallow_arrow import ArrowField

from ....models import Script


class ScriptSchema(Schema):
    model = Script

    id = fields.Integer()

    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=64),
            validate.Regexp(r'[\w]+')
        ]
    )

    tag = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=64),
            validate.Regexp(r'[\w]+')
        ]
    )

    calls = fields.Integer()

    runtime = fields.Integer()

    created_at = ArrowField()

    updated_at = ArrowField()

    owner_id = fields.Nested(
        'UserSchema',
        many=False
    )
