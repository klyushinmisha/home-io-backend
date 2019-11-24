from uuid import uuid4

from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import bindparam

from . import parser
from .. import api
from ..responses.device import *
from ..schemas import DeviceCreateSchema, DevicesReadSchema
from ..view_decorators import json_mimetype_required, PaginateResponse
from ...common.schemas import PaginationSchema
from ....models import Device, db


@api.route('/devices', methods=['GET'])
@jwt_required
@parser.use_kwargs(PaginationSchema, locations=('query',))
def get_devices(page, per_page):
    bq = Device.baked_query + (
        lambda q: q.filter(Device.owner_id == bindparam('owner_id'))
    )
    bq_params = {
        'owner_id': current_user.id
    }

    return PaginateResponse(
        bq,
        DevicesReadSchema,
        page,
        per_page,
        bq_params
    )


@api.route('/devices/<int:d_id>', methods=['GET'])
@jwt_required
def get_device(d_id):
    dev = Device.query.filter(
        Device.id == d_id
    ).one_or_none()
    if dev is None:
        return DeviceNotFoundResponse()
    elif dev.owner_id != current_user.id:
        return DeviceAccessDeniedResponse()
    return DeviceResponse(dev)


@api.route("/devices", methods=['POST'])
@json_mimetype_required
@parser.use_kwargs(DeviceCreateSchema, locations=('json',))
def create_new_device(uuid, name, owner_id):
    device = Device.query.filter(
        Device.name == name
    ).one_or_none()
    if device is not None:
        return DeviceAlreadyExistsResponse()

    if uuid is None:
        uuid = uuid4()

    device = Device(
        uuid=uuid,
        name=name,
        owner_id=owner_id,
    )
    db.session.add(device)
    db.session.commit()
    return DeviceResponse(device)
