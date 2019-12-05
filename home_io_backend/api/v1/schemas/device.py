from marshmallow import fields, Schema, validate
from marshmallow_arrow import ArrowField

from ...common.schemas import PaginationSchema
from ....models import Device


class DeviceSchema(Schema):
    model = Device

    uuid = fields.UUID(
        required=True
    )

    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=32),
            validate.Regexp(r'(^|,)[\w]+(,|$)', 0)
        ]
    )

    registered_at = ArrowField()


class DeviceGetSchema(PaginationSchema):
    nearby = fields.Boolean(
        missing=None
    )

    q = fields.String(
        missing=None
    )


class ConnectSchema(Schema):
    uuid = fields.UUID(
        required=True
    )

    password = fields.String()

