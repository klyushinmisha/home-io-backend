import uuid

import pytest

from ...models import Device, User, TypeEnum, DeviceTask
from ...api.v1.schemas import DeviceTaskReadSchema, DeviceTasksReadSchema, \
    DeviceTaskCreateSchema, DeviceTaskUpdateSchema, DeviceTasksReadSchema
from marshmallow.exceptions import ValidationError


@pytest.fixture(scope='function')
def device_task(app, db):
    with app.app_context():
        user = User(
            username='testuser',
            email='testuser@mail.com',
            password='TestPassword'
        )
        db.session.add(user)
        db.session.flush()

        device = Device(
            id=uuid.uuid4(),
            name='testdevice',
            device_type=TypeEnum.blinker,
            owner_id=user.id
        )
        db.session.add(device)
        db.session.flush()
        dev_task = DeviceTask(
            device_id=device.id,
            task={
                "task": "task1"
            }
        )
        db.session.add(dev_task)
        db.session.commit()
        return dev_task


class TestDeviceTaskReadSchema:
    def test_read(self, app, device_task):
        with app.app_context():
            dev_task = DeviceTask.query.all()[0]
            try:
                res = DeviceTaskReadSchema.dump(dev_task)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'


class TestDeviceTasksReadSchema:
    def test_read(self, app, device_task):
        with app.app_context():
            dev_task = DeviceTask.query.all()
            try:
                res = DeviceTaskReadSchema.dump(dev_task)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'


class TestDeviceTaskCreateSchema:
    @pytest.mark.parametrize(
        'task',
        [({"task": "task"},)]
    )
    def test_invalid_device_task(self, task):
        device_task_data = {
            'task': task,
        }
        try:
            DeviceTaskCreateSchema.load(device_task_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'task' in e.messages

    @pytest.mark.parametrize(
        'task',
        ({"task": "task"})
    )
    def test_valid_data(self, task):
        device_task_data = {
            'task': task,
        }
        try:
            DeviceTaskCreateSchema.load(device_task_data)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'

    @pytest.mark.parametrize(
        'id, task, created_at, device_id',
        (1, {"task": "task"}, 'ANYTIME', uuid.uuid4())
    )
    def test_pass_not_allowed_keys(self, id, task, created_at, device_id):
        device_task_data = {
            'id': id,
            'task': task,
            'created_at': created_at,
            'device_id': device_id,
        }
        try:
            DeviceTaskCreateSchema.load(device_task_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages
            assert 'device_id' in e.messages


class TestDeviceTaskUpdateSchema:
    @pytest.mark.parametrize(
        'id, created_at, device_id',
        ((1, 'ANYTIME', uuid.uuid4()),)
    )
    def test_pass_not_allowed_keys(self, id, created_at, device_id):
        device_task_data = {
            'id': id,
            'created_at': created_at,
            'device_id': device_id
        }
        try:
            DeviceTaskUpdateSchema.load(device_task_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages
            assert 'device_id' in e.messages

    @pytest.mark.parametrize(
        'task',
        (({"task": "task"}),)
    )
    def test_partial_update(self, task):
        device_task_data = {
            'task': task,
        }
        try:
            DeviceTaskUpdateSchema.load(device_task_data)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'