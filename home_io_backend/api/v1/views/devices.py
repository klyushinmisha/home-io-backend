import sqlalchemy as sa
from flask import request
from flask_jwt_extended import jwt_required, current_user, create_access_token
from sqlalchemy import bindparam
from sqlalchemy import or_, cast

from . import parser
from .. import api
from ..responses.device import *
from ..schemas import DeviceCreateSchema, DevicesReadSchema
from ..schemas.device import DeviceGetSchema, ConnectSchema
from ..view_decorators import json_mimetype_required, PaginateResponse
from ....models import Device, db


@api.route('/devices', methods=['GET'])
@jwt_required
@parser.use_kwargs(DeviceGetSchema(), locations=('query',))
def get_devices(q, nearby, page, per_page):
    bq = Device.baked_query + (
        lambda query: query.filter(Device.owner_id == bindparam('owner_id'))
    )
    bq_params = {
        'owner_id': current_user.id
    }

    if q is not None:
        bq += (lambda query: query.filter(
                or_(
                    Device.name.ilike(bindparam('q')),
                    cast(Device.uuid, sa.String).ilike(bindparam('q'))
                )
            )
        )
        bq_params.update({
            'q': q + '%'
        })

    if nearby:
        addr_mask = '.'.join(
            request.remote_addr.split('.')[0:3]
        )
        bq += (lambda query: query.filter(
            Device.last_address.ilike(bindparam('addr_mask'))
        ))
        bq_params.update({
            'addr_mask': addr_mask + '%'
        })

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
def create_new_device(uuid, name):
    device = Device.query.filter(
        Device.name == name
    ).one_or_none()
    if device is not None:
        return DeviceAlreadyExistsResponse()

    device = Device(
        uuid=uuid,
        name=name
    )
    current_user.devices.append(device)
    db.session.commit()
    return DeviceResponse(device)
