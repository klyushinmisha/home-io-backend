__all__ = [
    'DeviceLogReadSchema',
    'DeviceLogSchema'
]

from marshmallow import fields, validate, Schema, post_load
from marshmallow_arrow import ArrowField
from ....models import DeviceLog, Device
import json


class DeviceLogSchema(Schema):
    id = fields.Integer()

    log = fields.Raw(
        required=True
    )

    created_at = ArrowField()

    device_id = fields.Integer(
        required=True,
        validate=[
            lambda dev_id: Device.query.get(dev_id) is not None
        ]
    )

    @post_load()
    def create_device_log_object(self, data):
        data['log'] = json.loads(data["log"])
        return DeviceLog(**data)


DeviceLogReadSchema = DeviceLogSchema()
DevicesLogReadSchema = DeviceLogSchema(many=True)
DeviceLogCreateSchema = DeviceLogSchema(
    exclude=('id', 'created_at', 'device_id')
)
DeviceLogUpdateSchema = DeviceLogSchema(
    exclude=('id', 'created_at', 'device_id'),
    partial=True
)
