import json

import requests

from . import API_URL, TOKEN


class Device:
    def __init__(self, uuid, name=None):
        self.uuid = uuid
        self.name = name

    @staticmethod
    def get_by_uuid(dev_uuid):
        resp = requests.get(
            f'{API_URL}/devices',
            headers={
                'Authorization': f'Bearer {TOKEN}'
            }
        ).text
        dev_json = filter(
            lambda dev: dev['uuid'] == dev_uuid,
            json.loads(resp)['data']
        ).__next__()
        return Device(
            dev_json['uuid'],
            dev_json['name']
        )

    def push_task(self, task):
        requests.post(
            f'{API_URL}/devices/{self.uuid}/tasks',
            json={
                'device_id': self.uuid,
                'task': json.dumps(task)
            },
            headers={
                'Authorization': f'Bearer {TOKEN}'
            }
        )

    @property
    def logs(self):
        resp = requests.get(
            f'{API_URL}/devices/{self.uuid}/logs',
            headers={
                'Authorization': f'Bearer {TOKEN}'
            }
        ).text
        return list(map(
            lambda log: log['log'],
            json.loads(resp)
        ))
