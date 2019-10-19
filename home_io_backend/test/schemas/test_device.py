import uuid

import pytest

from ...models import Device, User, TypeEnum
from ...api.v1.schemas import DeviceReadSchema, DevicesReadSchema, \
    DeviceCreateSchema, DeviceUpdateSchema
from marshmallow.exceptions import ValidationError


@pytest.fixture(scope='function')
def device(app, db):
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
        db.session.commit()
        return device


class TestDeviceReadSchema:
    def test_read(self, app, device):
        with app.app_context():
            device = Device.query.all()[0]
            try:
                res = DeviceReadSchema.dump(device)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'


class TestDeviceCreateSchema:
    @pytest.mark.parametrize(
        'name, device_type',
        (('tet', 'blinker'),
         ('fdsfsd', 'tetrshhgfh'),
         ('very_long_devname_very_long_devname_very_long', 'blinker'),
         ('@@@@@#####----', 'blinker'),)
    )
    def test_invalid_device(self, name, device_type):
        device_data = {
            'name': name,
            'device_type': device_type,
        }
        try:
            DeviceCreateSchema.load(device_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'name' or 'device_name' in e.messages

    @pytest.mark.parametrize(
        'name, device_type',
        (('test_device', 'blinker', ),)
    )
    def test_valid_data(self, name, device_type):
        device_data = {
            'name': name,
            'device_type': device_type,
        }
        try:
            DeviceCreateSchema.load(device_data)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'

    @pytest.mark.parametrize(
        'id, name, device_type, owner_id, registred_at',
        ((uuid.uuid4(), 'test_device', 'blinker', 1, 'ANYTIME'),)
    )
    def test_pass_not_allowed_keys(self, id, name, device_type, owner_id, registred_at):
        device_data = {
            'id': id,
            'name': name,
            'device_type': device_type,
            'owner_id': owner_id,
            'registred_at': registred_at
        }
        try:
            DeviceCreateSchema.load(device_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'registred_at' in e.messages
            assert 'owner_id' in e.messages


class TestDeviceUpdateSchema:
    @pytest.mark.parametrize(
        'id, registred_at',
        ((uuid.uuid4(), 'ANYTIME'),)
    )
    def test_pass_not_allowed_keys(self, id, registred_at):
        device_data = {
            'id': id,
            'registred_at': registred_at
        }
        try:
            DeviceUpdateSchema.load(device_data)
            assert False, 'Exception must occur'
        except ValidationError as e:
            assert 'id' in e.messages
            assert 'registred_at' in e.messages

    @pytest.mark.parametrize(
        'name, device_type',
        (('test_device', 'blinker'),)
    )
    def test_partial_update(self, name, device_type):
        device_data = {
            'name': name,
            'device_type':device_type
        }
        try:
            DeviceUpdateSchema.load(device_data)
        except ValidationError as e:
            assert False, 'Can`t be ValidationError'


class TestDevicesReadSchema:
    def test_read(self, app, device):
        with app.app_context():
            devices = Device.query.all()
            try:
                res = DevicesReadSchema.dump(devices)
            except ValidationError as e:
                assert False, 'Can`t be ValidationError'
