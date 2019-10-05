from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext import baked

db = SQLAlchemy()
db.bakery = baked.bakery()

from .user import User
from .device import Device
from .device_log import DeviceLog
from .device_task import DeviceTask

__all__ = [
    'db',
    'User',
    'Device',
    'DeviceLog',
    'DeviceTask'
]