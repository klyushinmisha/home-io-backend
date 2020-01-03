from marshmallow import fields, Schema
from marshmallow_arrow import ArrowField

from ....models import DeviceLog


class DeviceLogSchema(Schema):

    model = DeviceLog

    id = fields.Integer()

    log = fields.Raw(
        required=True
    )

    tag = fields.String(
        required=True
    )

    created_at = ArrowField()

    # FIXME: remove
    device_id = fields.UUID(
        required=False
    )
