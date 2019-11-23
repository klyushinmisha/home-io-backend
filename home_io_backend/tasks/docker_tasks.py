import os
import shutil
import time

import docker

from .. import celery
from ..hash_utils import hash_build_name

BUILDS_POOL = os.environ.get('BUILDS_POOL')
HOME_IO_SDK_PATH = os.environ.get('HOME_IO_SDK_PATH')
DOCKERFILE_PATH = os.environ.get('DOCKERFILE_PATH')
DOCKER_MACHINE_URL = os.environ.get('DOCKER_MACHINE_URI')

client = docker.DockerClient(base_url=DOCKER_MACHINE_URL)        # TODO: pass TCP socket from VM


@celery.task
def build_container(name, tag, script_path):
    # TODO: add versions
    container_tag = f'{name}/{tag}:latest'
    sha_id = hash_build_name(name, tag)
    build_path = os.path.join(
        BUILDS_POOL,
        sha_id
    )

    if os.path.exists(build_path):
        shutil.rmtree(build_path)
        # NOTE: wait some time for OS to remove tree
        time.sleep(0.5)
    os.makedirs(build_path, exist_ok=True)

    shutil.copyfile(
        script_path,
        os.path.join(
            build_path,
            'script.py'
        )
    )

    shutil.copytree(
        HOME_IO_SDK_PATH,
        os.path.join(
            build_path,
            'home_io_sdk'
        )
    )
    shutil.copyfile(
        DOCKERFILE_PATH,
        os.path.join(
            build_path,
            'Dockerfile'
        )
    )

    client.images.build(path=build_path, tag=container_tag)


@celery.task
def clean_containers():
    pass
