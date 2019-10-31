from webargs.flaskparser import use_kwargs

from .. import api
from ..responses.device import *
from ..schemas import DeviceCreateSchema
from ..view_decorators import json_mimetype_required
from ....models import Device, db


@api.route("/devices", methods=['POST'])
@json_mimetype_required
@use_kwargs(DeviceCreateSchema, locations=('json',))
def create_new_device(device_id, name, device_type, owner_id):
    device = Device.query.filter(
        Device.name == name
    ).one_or_none()
    if device is not None:
        return DeviceAlreadyExistResponse()
    device = Device(
        id=device_id,
        name=name,
        device_type=device_type,
        owner_id=owner_id,
    )
    db.session.add(device)
    db.session.commit()
    return DeviceResponse(device)
