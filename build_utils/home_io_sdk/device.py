import os

import requests

from . import API_URL


class Device:
    @staticmethod
    def by_name(name):
        resp = requests.get(
            f'{API_URL}/devices',
            headers={
                'authorization': os.environ.get('ACCESS_TOKEN')
            }
        )
        print(resp.text)
