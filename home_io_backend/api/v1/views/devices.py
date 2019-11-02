from webargs.flaskparser import use_kwargs
from flask_jwt_extended import jwt_required, current_user
from ..schemas.utils import update_instance
from flask import request
from . import parser

from .. import api
from ..responses.device import *
from ..schemas import DeviceCreateSchema, DeviceUpdateSchema
from ..view_decorators import json_mimetype_required
from ....models import Device, db, TypeEnum


@api.route("/devices", methods=['POST'])
@json_mimetype_required
@parser.use_kwargs(DeviceCreateSchema, locations=('json',))
def create_new_device(id, name, device_type, owner_id):
    device = Device.query.filter(
        Device.name == name
    ).one_or_none()
    if device is not None:
        return DeviceAlreadyExistResponse()
    device = Device(
        id=id,
        name=name,
        device_type=TypeEnum(device_type),
        owner_id=owner_id,
    )
    db.session.add(device)
    db.session.commit()
    return DeviceResponse(device)


@api.route("/devices/<int:d_id>", methods=['GET'])
@jwt_required
def get_device(d_id):
    device = Device.query.get(d_id)
    if device is None:
        return DeviceNotFoundResponse()
    return DeviceResponse(device)


@api.route("/devices/<int:d_id>", methods=["DELETE"])
@jwt_required
def delete_device(d_id):
    device = Device.query.get(d_id)
    if device is None:
        return DeviceNotFoundResponse()
    db.session.remove(device)
    db.session.commit()
    return DeviceDeleteSuccessfullyResponse(device)


@api.route("/devices/<int:d_id>", methods=["PATCH"])
@jwt_required
def update_device(d_id):
    device = Device.query.get(d_id)
    if device is None:
        return DeviceNotFoundResponse()
    update_instance(DeviceUpdateSchema, request.json, device)
    db.session.commit()
    return DeviceUpdateSuccessfullyResponse(device)
