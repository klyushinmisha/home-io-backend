from flask import request
from flask_jwt_extended import create_access_token, jwt_required, current_user

from .. import api
from ..responses.device import *
from ..schemas import DeviceLogsCreateSchema, ScriptRunSchema
from ..view_decorators import json_mimetype_required
from ....models import Device, db, Script
from ....tasks.docker_tasks import run_image


@api.route("/logs", methods=['POST'])
@jwt_required
@json_mimetype_required
def process_logs():
    device = Device.query\
        .filter(Device.uuid == current_user.id)\
        .one_or_none()
    if device is None:
        return DeviceNotFoundResponse()

    logs = DeviceLogsCreateSchema.load(request.json)

    # TODO: order by created_at
    for log in logs:
        db.session.add(log)
    db.session.commit()

    access_token = create_access_token(
        identity=device.user.username
    )
    tags = set(map(lambda l: l.tag, logs))
    for tag in tags:
        script = Script.query\
            .filter(Script.tag == tag)\
            .one_or_none()
        if script is None:
            #TODO: add error report for all failed starts
            pass
        else:
            run_data = ScriptRunSchema.dump(script)
            name = run_data['name']
            tag = run_data['tag']

            run_image.delay(name, tag, access_token)
