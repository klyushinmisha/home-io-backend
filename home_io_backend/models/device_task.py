import arrow
from sqlalchemy_utils import JSONType, ArrowType

from . import db


class DeviceTask(db.Model):

    __tablename__ = 'device_task'

    baked_query = db.bakery(lambda session: session.query(DeviceTask))

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
        unique=True
    )

    device_id = db.Column(
        db.ForeignKey(
            'device.id',
            ondelete='CASCADE'
        ),
        nullable=False
    )

    task = db.Column(
        JSONType,
        nullable=False
    )

    created_at = db.Column(
        ArrowType,
        default=arrow.utcnow
    )
