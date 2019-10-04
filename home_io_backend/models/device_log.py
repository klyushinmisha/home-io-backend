import arrow
from sqlalchemy_utils import ArrowType, JSONType, UUIDType

from . import db


class DeviceLog(db.Model):
    __tablename__ = "device_log"

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
        unique=True
    )

    log = db.Column(
        JSONType,
        nullable=False
    )

    created_at = db.Column(
        ArrowType,
        default=arrow.utcnow
    )

    device_id = db.Column(
        db.ForeignKey('device.id'),
        cascade="all, delete-orphan",
        nullable=False
    )