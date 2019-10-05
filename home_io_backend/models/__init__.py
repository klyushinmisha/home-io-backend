from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .device import Device
from .device_log import DeviceLog
from .device_task import DeviceTask
