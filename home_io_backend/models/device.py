import enum

import arrow
from sqlalchemy import Enum
from sqlalchemy_utils import ArrowType, UUIDType

from . import db
from .device_log import DeviceLog
from .device_task import DeviceTask


class TypeEnum(enum.Enum):
    humidity_sensor = 0
    blinker = 1
    rangefinder = 2


class Device(db.Model):

    __tablename__ = 'device'

    baked_query = db.bakery(lambda session: session.query(Device))

    id = db.Column(
        UUIDType(binary=True),
        nullable=False,
        primary_key=True,
        unique=True,
    )

    name = db.Column(
        db.String(128),
        nullable=False
    )

    registered_at = db.Column(
        ArrowType,
        default=arrow.utcnow,
        onupdate=arrow.utcnow
    )

    device_type = db.Column(Enum(TypeEnum))

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False
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
