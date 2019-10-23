__all__ = [
    'DeviceLogReadSchema',
    'DevicesLogReadSchema',
    'DeviceLogCreateSchema',
    'DeviceLogUpdateSchema',
]

import json

from marshmallow import fields, validate, Schema
from marshmallow_arrow import ArrowField

from ....models import Device, DeviceLog


class DeviceLogSchema(Schema):

    model = DeviceLog

    id = fields.Integer()

    log = fields.Raw(
        required=True
    )

    created_at = ArrowField()

    device_id = fields.UUID(
        required=True,
        validate=[
            lambda dev_id: Device.query.get(dev_id) is not None
        ]
    )
