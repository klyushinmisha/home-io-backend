import pytest
import uuid
from ...models import DeviceLog
from ...api.v1.schemas import DeviceLogReadSchema, DeviceLogsReadSchema, \
    DeviceLogCreateSchema, DeviceLogsCreateSchema, DeviceLogUpdateSchema
from marshmallow.exceptions import ValidationError
import arrow


@pytest.fixture(scope='function')
def dev_log(app, db):
    with app.app_context():
        # create user to read
        dev_log = DeviceLog(
            device_id= uuid.UUID("ffebed83-957b-49e4-ba70-b1b1f53004ad"),
            log = {"logs" : "test"}
        )
        db.session.add(dev_log)
        db.session.commit()
        return dev_log


class TestDeviceLogReadSchema:
    def test_read(self, app):
        with app.app_context():
            dev_log = DeviceLog.query.all()[0]
            try:
                res = DeviceLogReadSchema.dump(dev_log)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'


class TestDeviceLogCreateSchema:
    @pytest.mark.parametrize(
        'device_id, log',
        (('ffebed83-957b-49e4-ba70-b1b1f53004ad', {"log": "test"}),
         ('edec2e3c-30c7-475e-aa3b-44642cf7c5a0', {"idi": "kukuruzu_ohranyai"}),
         ('febf8c05-6fc1-4834-8ee4-998420dd2d1a', {"access": "success"}),)
    )
    def test_invalid_device_id(self, device_id, log):
        dev_log = {
            'device_id': device_id,
            'log': log
        }
        try:
            DeviceLogCreateSchema.load(dev_log)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'device_id' in e.messages

    @pytest.mark.parametrize(
        'device_id, log',
        (('ffebed83-957b-49e4-ba70-b1b1f53004ad', {"log": "test"}),
         ('edec2e3c-30c7-475e-aa3b-44642cf7c5a0', {"idi": "kukuruzu_ohranyai"}),
         ('febf8c05-6fc1-4834-8ee4-998420dd2d1a', {"access": "success"}),)
    )
    def test_invalid_email(self, device_id, log):
        dev_log = {
            'device_id': device_id,
            'log': log
        }
        try:
            DeviceLogCreateSchema.load(dev_log)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'log' in e.messages


    @pytest.mark.parametrize(
        'id, created_at, device_id, log',
        ((1,arrow.now() , 'mail@mail.com', 'edec2e3c-30c7-475e-aa3b-44642cf7c5a0', {"you_are": "gay"}), )
    )
    def test_pass_not_allowed_keys(self, id, created_at, device_id, log):
        dev_log = {
            'id': id,
            'created_at': created_at,
            'device_id': device_id,
            'log': log,
        }
        try:
            DeviceLogCreateSchema.load(dev_log)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages

    @pytest.mark.parametrize(
        'device_id, log',
        ('ffebed83-957b-49e4-ba70-b1b1f53004ad', {"log": "test"}))
    def test_valid_data(self, device_id, log):
        dev_log = {
            'device_id': device_id,
            'log': log,
        }
        try:
            DeviceLogCreateSchema.load(dev_log)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'


class TestUserUpdateSchema:
    @pytest.mark.parametrize(
        'device_id, created_at',
        (("ffebed83-957b-49e4-ba70-b1b1f53004ad", arrow.now()), )
    )
    def test_pass_not_allowed_keys(self, device_id, created_at):
        dev_log = {
            'device_id': device_id,
            'created_at': created_at
        }
        try:
            DeviceLogUpdateSchema.load(dev_log)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'created_at' in e.messages

    @pytest.mark.parametrize(
        'id',
        ((5), )
    )
    def test_partial_update(self, id):
        dev_log = {
            'id': id,
        }
        try:
            DeviceLogUpdateSchema.load(dev_log)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'


class TestUsersReadSchema:
    def test_read(self, app):
        with app.app_context():
            dev_logs = DeviceLog.query.all()
            try:
                res = DeviceLogReadSchema.dump(dev_logs)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'