from marshmallow import fields, validate, Schema
from marshmallow_arrow import ArrowField
from marshmallow_enum import EnumField

from ....models import Device, TypeEnum


class DeviceSchema(Schema):
    model = Device

    id = fields.UUID()

    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=32),
            validate.Regexp(r'[\w]+')
        ]
    )

    registered_at = ArrowField()

    device_type = EnumField(
        TypeEnum,
        validate=validate.OneOf(
            [
                TypeEnum.blinker,
                TypeEnum.humidity_sensor,
                TypeEnum.rangefinder
            ]
        ), required=True
    )

    owner_id = fields.Nested(
        'UserSchema',
        many=False
    )
