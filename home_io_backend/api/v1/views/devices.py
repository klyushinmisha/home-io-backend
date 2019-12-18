import arrow
import sqlalchemy as sa
from flask import request
from flask_jwt_extended import jwt_required, current_user, create_access_token
from sqlalchemy import bindparam
from sqlalchemy import or_, cast

from . import parser
from .. import api
from ..responses.device import *
from ..schemas import DeviceCreateSchema, DevicesReadSchema, DeviceLogsCreateSchema, ScriptRunSchema, \
    DeviceLogsReadSchema, DeviceTaskCreateSchema
from ..schemas.device import DeviceGetSchema
from ..view_decorators import json_mimetype_required, PaginateResponse
from ....models import Device, db, Script, DeviceLog, DeviceTask
from ....tasks.docker_tasks import run_image


@api.route('/devices', methods=['GET'])
@jwt_required
@parser.use_kwargs(DeviceGetSchema(), locations=('query',))
def get_devices(q, nearby, page, per_page):
    bq = Device.baked_query + (
        lambda query: query.filter(Device.user_id == bindparam('user_id'))
    )
    bq_params = {
        'user_id': current_user.id
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
    elif dev.user_id != current_user.id:
        return DeviceAccessDeniedResponse()
    return DeviceResponse(dev)


@api.route("/devices", methods=['POST'])
@jwt_required
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
        name=name,
        user_id=current_user.id
    )
    db.session.add(device)
    db.session.commit()
    return DeviceResponse(device)


@api.route('/devices/<uuid:dev_uuid>/logs', methods=['POST'])
@jwt_required
@json_mimetype_required
def post_log(dev_uuid):
    device = Device.query \
        .filter(
            Device.uuid == dev_uuid,
            Device.user_id == current_user.id
        ) \
        .one_or_none()
    if device is None:
        return DeviceNotFoundResponse()

    logs = DeviceLogsCreateSchema.load(request.json)

    # TODO: order by created_at
    for log in logs:
        log_inst = DeviceLog(
            log=log['log'],
            device_id=device.id
        )
        db.session.add(log_inst)
    db.session.commit()

    access_token = create_access_token(
        identity=current_user.username
    )
    # TODO: add load balancing
    tags = set(map(lambda l: l['tag'], logs))
    for tag in tags:
        script = Script.query \
            .filter(Script.tag == tag) \
            .one_or_none()
        if script is None:
            # TODO: add error report for all failed starts
            pass
        elif script.enabled:
            run_data = ScriptRunSchema.dump(script)
            name = run_data['name']
            tag = run_data['tag']

            # TODO: add runtime calculation
            run_image.delay(name, tag, access_token)

            script.calls = script.calls + 1
            db.session.commit()
    return DeviceScriptsStartedResponse()


@api.route('/devices/<uuid:dev_uuid>/logs', methods=['GET'])
@jwt_required
def get_log(dev_uuid):
    device = Device.query \
        .filter(
            Device.uuid == dev_uuid,
            Device.user_id == current_user.id
        ) \
        .one_or_none()
    if device is None:
        return DeviceNotFoundResponse()

    logs = DeviceLogsReadSchema.dump(device.logs)

    return DeviceLogsResponse(logs)


@api.route('/devices/<uuid:dev_uuid>/tasks', methods=['POST'])
@jwt_required
@json_mimetype_required
def post_tasks(dev_uuid):
    device = Device.query \
        .filter(
            Device.uuid == dev_uuid,
            Device.user_id == current_user.id
        ).one_or_none()
    if device is None:
        return DeviceNotFoundResponse()

    task = DeviceTaskCreateSchema.load(request.json)
    task_inst = DeviceTask(
        task=task['task'],
        device_id=device.id
    )
    db.session.add(task_inst)
    db.session.commit()

    return DeviceTaskCreatedResponse()


@api.route('/devices/<uuid:dev_uuid>/tasks', methods=['GET'])
@jwt_required
def get_tasks(dev_uuid):
    device = Device.query \
        .filter(
            Device.uuid == dev_uuid,
            Device.user_id == current_user.id
        ).one_or_none()
    if device is None:
        return DeviceNotFoundResponse()

    resp = DeviceTasksResponse(device.device_tasks)
    device_tasks = DeviceTask.query.filter(
        DeviceTask.device_id == device.id
    )
    device_tasks.delete()
    db.session.commit()

    return resp
