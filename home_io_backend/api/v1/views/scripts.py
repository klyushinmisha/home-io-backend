__all__ = [
    'get_scripts',
    'create_script',
    'get_script',
    'update_script',
    'delete_script'
]

import os

from flask import request, current_app
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import bindparam

from home_io_backend.tasks.docker_tasks import build_container
from . import parser
from .. import api
from ..responses.script import *
from ..schemas import ScriptUpdateSchema, ScriptsReadSchema, \
    ScriptCreateSchema, ScriptBuildSchema
from ..schemas.utils import update_instance
from ..view_decorators import json_mimetype_required
from ...common.responses import PaginateResponse
from ...common.schemas import PaginationSchema
from ....hash_utils import hash_build_name
from ....models import db, Script


@api.route('/scripts', methods=['GET'])
@jwt_required
@parser.use_kwargs(PaginationSchema(), locations=('query',))
def get_scripts(page, per_page):
    bq = Script.baked_query + (
        lambda q: q.filter(Script.user_id == bindparam('user_id'))
    )
    bq_params = {
        'user_id': current_user.id
    }

    return PaginateResponse(
        bq,
        ScriptsReadSchema,
        page,
        per_page,
        bq_params
    )


@api.route('/scripts', methods=['POST'])
@jwt_required
@json_mimetype_required
@parser.use_kwargs(ScriptCreateSchema, locations=('json',))
def create_script(name, tag, code):
    # check ability to create script
    bq = Script.baked_query + (lambda q: q
        .filter(Script.tag == bindparam('tag')))
    bq_params = {
        'tag': tag
    }
    script = bq(db.session()).params(bq_params).one_or_none()
    if script is not None:
        return ScriptTagAlreadyExistsResponse()

    # NOTE: save file first.
    # If something gets wrong, then celery job will clear files
    folder_name = hash_build_name(name, tag)
    script_folder_path = os.path.join(
        current_app.config['SCRIPTS_PATH'],
        folder_name
    )
    os.makedirs(script_folder_path, exist_ok=True)
    script_path = os.path.join(script_folder_path, 'script.py')
    with open(script_path, 'w') as s:
        s.write(code)

    script = Script(
        name=name,
        tag=tag,
        user_id=current_user.id
    )
    db.session.add(script)
    db.session.commit()
    return ScriptResponse(script)


@api.route('/scripts/<int:s_id>/build', methods=['POST'])
@jwt_required
def build_script(s_id):
    script = Script.query.get(s_id)

    if script is None:
        return ScriptNotFoundResponse()
    if script.user_id != current_user.id:
        return ScriptAccessDeniedResponse()

    build_data = ScriptBuildSchema.dump(script)
    name = build_data['name']
    tag = build_data['tag']
    script_folder = hash_build_name(name, tag)
    script_path = os.path.join(
        current_app.config['SCRIPTS_PATH'],
        script_folder,
        'script.py'
    )

    build_container.delay(name, tag, script_path)
    return ScriptBuildStartedResponse()


@api.route('/scripts/<int:s_id>/switch_enabled', methods=['POST'])
@jwt_required
def enable_script(s_id):
    script = Script.query.get(s_id)

    if script is None:
        return ScriptNotFoundResponse()
    if script.user_id != current_user.id:
        return ScriptAccessDeniedResponse()

    script.enabled = not script.enabled
    db.session.commit()
    return ScriptEnableSwitchedResponse()


@api.route('/scripts/<int:s_id>', methods=['GET'])
@jwt_required
def get_script(s_id):
    script = Script.query.get(s_id)
    if script is None:
        return ScriptNotFoundResponse()
    if script.user_id != current_user.id:
        return ScriptAccessDeniedResponse()
    folder_name = hash_build_name(
        script.name,
        script.tag
    )
    script_folder_path = os.path.join(
        current_app.config['SCRIPTS_PATH'],
        folder_name
    )
    script_path = os.path.join(script_folder_path, 'script.py')
    with open(script_path, 'r') as s:
        code = s.read()
    return ScriptResponse(script, code)


@api.route('/scripts/<int:s_id>', methods=['PATCH'])
@jwt_required
def update_script(s_id):
    script = Script.query.get(s_id)
    if script.user_id != current_user.id:
        return ScriptAccessDeniedResponse()
    update_instance(ScriptUpdateSchema, script, request.json)
    db.session.commit()
    return ScriptResponse(script)


@api.route('/scripts/<int:s_id>', methods=['DELETE'])
@jwt_required
def delete_script(s_id):
    script = Script.query.get(s_id)
    if script.user_id != current_user.id:
        return ScriptAccessDeniedResponse()
    db.session.remove(script)
    db.session.commit()
    return ScriptDeleteResponse(script)
