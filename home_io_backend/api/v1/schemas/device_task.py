from marshmallow import fields, Schema
from marshmallow_arrow import ArrowField

from ....models import DeviceTask


class DeviceTaskSchema(Schema):
    model = DeviceTask

    id = fields.Integer()

    task = fields.Raw(
        required=True
    )
    created_at = ArrowField()

    # FIXME: remove
    device_id = fields.UUID(
        required=False
    )
