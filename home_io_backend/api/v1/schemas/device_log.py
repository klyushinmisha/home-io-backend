__all__ = [
    'DeviceLogReadSchema',
    'DeviceLogSchema'
]

from marshmallow import fields, validate, Schema, post_load
from marshmallow_arrow import ArrowField
from ....models import DeviceLog
import json


class DeviceLogSchema(Schema):
    id = fields.Integer()

    log = fields.Dict(
        required=True)

    created_at = ArrowField()

    device_id = fields.Nested(
        'device.id',
        required=True,
        exclude='user,'
    )

    @post_load()
    def create_device_log_object(self, data):
        return DeviceLog(
            id=data["id"],
            log=json.loads(data["log"]),
            created_at=data["created_at"],
            device_id=data["device_id"]
        )


DeviceLogReadSchema = DeviceLogSchema()
DevicesLogReadSchema = DeviceLogSchema(many=True)
'''
DeviceLogCreateSchema = DeviceLogSchema(
    exclude=('id', 'created_at', 'devices')
) '''
'''
DeviceLogUpdateSchema = DeviceLogSchema(
    exclude=('id', 'log', 'created_at'),
    partial=True
)'''
