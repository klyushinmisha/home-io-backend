import pytest
from ...models.device import Device, TypeEnum
from ...models import User
from sqlalchemy import bindparam


@pytest.fixture(scope='function')
def device_id(app, db):
    with app.app_context():
        u = User(
            username='testuser',
            email='testuser@mail.com',
            password='TestPassword'
        )
        db.session.add(u)
        db.session.flush()
        
        # create device to read
        d = Device(
            name='testdevice',
            device_type=TypeEnum.blinker,
            owner_id=u.id
        )
        u.devices.append(d)
        db.session.commit()
        return d.id


class TestDevice:
    @pytest.mark.parametrize(
        'name,device_type',
        (('testdevice', TypeEnum.blinker),
         ('device', TypeEnum.humidity_sensor))
    )
    def test_create(self, app, db, name, device_type):
        with app.app_context():
            u = User(
                username='testuser',
                email='testuser@mail.com',
                password='TestPassword'
            )
            db.session.add(u)
            db.session.flush()

            d = Device(
                name=name,
                device_type=device_type
            )
            u.devices.append(d)
            db.session.commit()

    def test_read(self, app, db, device_id):
        with app.app_context():
            # try to read device
            bq = Device.baked_query + (lambda q: q
                .filter(Device.id == bindparam('device_id'))
            )
            bq_params = {
                'device_id': device_id
            }
            d = (bq(db.session())
                .params(bq_params)
                .one_or_none())
            assert d is not None

    @pytest.mark.parametrize(
        'name, device_type',
        (('newname', TypeEnum.humidity_sensor),)
    )
    def test_update(self, app, db, name, device_type, device_id):
        with app.app_context():
            # read user
            bq = Device.baked_query + (lambda q: q
                .filter(Device.id == bindparam('device_id'))
            )
            bq_params = {
                'device_id': device_id
            }
            d = (bq(app.db.session())
                .params(bq_params)
                .one_or_none())

            # update device data
            d.name = name
            d.device_type = device_type
            db.session.add(d)
            db.session.commit()

    def test_delete(self, app, db, device_id):
        with app.app_context():
            # read device
            bq = Device.baked_query + (lambda q: q
                .filter(Device.id == bindparam('device_id'))
            )
            bq_params = {
                'device_id': device_id
            }
            d = (bq(db.session())
                .params(bq_params)
                .one_or_none())
            
            # delete device
            db.session.delete(d)
            db.session.commit()
