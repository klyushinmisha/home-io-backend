import pytest
from sqlalchemy import bindparam
from sqlalchemy_utils import JSONType, ArrowType
from ...models import DeviceLog, Device, User, TypeEnum, DeviceTask

@pytest.fixture(scope='function')
def device_id(app, db):
    with app.app_context():
        user = User(email="hi@gmail.com", username="newUser", password="password")
        db.session.add(user)
        db.session.flush()
        dev = Device(name="deviceD", device_type=TypeEnum.blinker, owner_id=user.id)
        db.session.add(dev)
        db.session.flush()
        devTask = DeviceTask(device_id=dev.id, task={"task": "mainTask"})
        db.session.add(devTask)
        db.session.commit()
        return devTask.device_id


class TestDeviceTask():
    def test_create_and_get(self,app, db):
        with app.app_context():
            user = User(email = "privet@gmail.com", username="mainUser",  password = "password")
            db.session.add(user)
            db.session.flush()
            dev = Device(name = "deviceName", device_type = TypeEnum.blinker, owner_id= user.id)
            db.session.add(dev)
            db.session.flush()
            devTask = DeviceTask(device_id= dev.id, task = {"task" : "mainTask"})
            db.session.add(devTask)
            db.session.commit()
            sameDevTask = DeviceTask.query.filter_by(device_id=devTask.id).first()
            assert sameDevTask is devTask


    def test_read(self, app, db, device_id):
        with app.app_context():
            # read user
            bq = DeviceTask.baked_query + (lambda q: q
                                       .filter(DeviceTask.id == bindparam('device_id'))
                                       )
            bq_params = {
                'device_id': device_id
            }
            devTask = (bq(app.db.session())
                       .params(bq_params)
                       .one_or_none())

            # update device data
        assert devTask is not None
    def test_update(self, app, db, device_id):
        with app.app_context():
            # read user
            bq = DeviceTask.baked_query + (lambda q: q
                                       .filter(DeviceTask.id == bindparam('device_id'))
                                       )
            bq_params = {
                'device_id': device_id
            }
            devTask = (bq(app.db.session())
                 .params(bq_params)
                 .one_or_none())

            # update device data

            devTask.task = {"key" : "prohodiNeZaderzhivaysya"}
            db.session.add(devTask)
            db.session.commit()

    def test_delete(self, app, db, device_id):
        with app.app_context():
            # read user
            bq = DeviceTask.baked_query + (lambda q: q
                                       .filter(DeviceTask.id == bindparam('device_id'))
                                       )
            bq_params = {
                'device_id': device_id
            }
            devTask = (bq(app.db.session())
                       .params(bq_params)
                       .one_or_none())

            # update device data
            db.session.delete(devTask)
            db.session.commit()

















