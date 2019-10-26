from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.ext import baked

db = SQLAlchemy()
db.bakery = baked.bakery()

bcrypt = Bcrypt()

from .user import User
from .device import Device, TypeEnum
from .device_log import DeviceLog
from .device_task import DeviceTask

__all__ = [
    'db',
    'User',
    'Device',
    'DeviceLog',
    'DeviceTask',
    'TypeEnum'
]
