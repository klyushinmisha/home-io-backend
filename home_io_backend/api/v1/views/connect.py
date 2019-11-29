from flask import request
from flask_jwt_extended import create_access_token

from . import parser
from .. import api
from ..responses.device import *
from ..schemas.device import ConnectSchema
from ..view_decorators import json_mimetype_required
from ....models import Device, db


@api.route("/connect", methods=['POST'])
@json_mimetype_required
@parser.use_kwargs(ConnectSchema(), locations=('json',))
def connect_device(uuid):
    device = Device.query\
        .filter(Device.uuid == uuid)\
        .one_or_none()
    if device is None:
        return DeviceNotFoundResponse()

    access_token = create_access_token(identity=uuid)

    device.last_address = request.remote_addr
    db.session.add(device)
    db.session.commit()
    return DeviceConnectedResponse(access_token)
