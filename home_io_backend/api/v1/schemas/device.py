from marshmallow import fields, validate, Schema
from marshmallow_arrow import ArrowField
from ....models import TypeEnum


class DeviceSchema(Schema):
    id = fields.UUID()

    name = fields.String(
        required=True,
        validate=[
            validate.Length(min=4, max=32),
            validate.Regexp(r"[\w]+")
        ]
    )

    registred_at = ArrowField()

    device_type = fields.Int(validate=validate.OneOf(
        [
            TypeEnum.blinker,
            TypeEnum.humidity_sensor,
            TypeEnum.rangefinder
        ]
    ), required=True)

    owner_id = fields.Nested(
        'UserSchema',
        many=False
    )

    device_logs = fields.Nested(
        'DeviceLogSchema',
        many=True
    )

    device_tasks = fields.Nested(
        'DeviceTaskSchema',
        many=True
    )


DeviceReadSchema = DeviceSchema()
DevicesReadSchema = DeviceSchema(many=True)
DeviceCreateSchema = DeviceSchema(
    exclude=('id', 'registred_at','owner_id', 'device_logs', 'device_tasks')
)
DeviceUpdateSchema = DeviceSchema(
    exclude=('id', 'registred_at', 'ownder_id', 'device_logs', 'device_tasks'),
    partial=True
)