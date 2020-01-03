import arrow
from sqlalchemy_utils import ArrowType, UUIDType

from . import db
from .device_log import DeviceLog
from .device_task import DeviceTask


class Device(db.Model):

    __tablename__ = 'device'

    baked_query = db.bakery(lambda session: session.query(Device))

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    uuid = db.Column(
        UUIDType(binary=False),
        nullable=False,
        unique=True,
        index=True
    )

    name = db.Column(
        db.String(128),
        index=True
    )

    last_address = db.Column(
        db.String(15),
        index=True
    )

    registered_at = db.Column(
        ArrowType,
        default=arrow.utcnow,
        index=True
    )

    user_id = db.Column(
        db.ForeignKey(
            'user.id',
            ondelete='CASCADE'
        ),
        nullable=True
    )

    device_logs = db.relationship(
        DeviceLog,
        backref='device',
        cascade='all, delete-orphan'
    )

    device_tasks = db.relationship(
        DeviceTask,
        backref='device',
        cascade='all, delete-orphan'
    )
