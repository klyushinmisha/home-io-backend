import os

API_URL = os.environ.get('API_URL')
TOKEN = os.environ.get('ACCESS_TOKEN')

from .device import Device
