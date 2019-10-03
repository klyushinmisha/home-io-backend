from . import db
from sqlalchemy_utils import ArrowType
from sqlalchemy_utils import UUIDType
from sqlalchemy import Enum
from .user import User
import uuid
import enum


class TypeEnum(enum.Enum):
    humidity_sensor = 1
    blinker = 2
    rangefinder = 3


class Device(db.Model):

    __tablename__ = "device"

    id = db.Column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        nullable=False
    )
    name = db.Column(db.String(128), nullable=False)
    registred_at = db.Column(ArrowType, nullable=False)
    type = db.Column(Enum(TypeEnum))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), cascade="all, delete-orphan")


