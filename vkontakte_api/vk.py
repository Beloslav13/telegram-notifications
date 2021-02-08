import datetime
import time

import requests
from pprint import pprint
import os


class Vkontakte:
    TOKEN_VK = os.environ.get("TOKEN_VK", '')
    BASE_URL = 'https://api.vk.com/method/{}?{}&v=5.52&access_token={}'

    def get_data(self, method, id, token, offset=0):
        try_connection = 3
        while try_connection:
            try:
                response = requests.get(self.BASE_URL.format(method, id, token), params={
                    "count": 5,
                    "offset": offset
                }).json()
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
                try_connection -= 1
                time.sleep(2)
                continue
            else:
                print('====Success request get====')
                return response
        else:
            raise requests.exceptions.ConnectionError(f'Max retries exceeded with url: {self.BASE_URL.format(method, id, token)}')

    # 568250150
    def get_pub(self, method, id, token):
        offset = 0
        has_next = True
        result = []
        while has_next:
            try:
                items = self.get_data(method, id, token, offset=offset)
            except requests.exceptions.ConnectionError as exc:
                print(f'Error: {exc}')
            else:
                if not items['response']['items']:
                    break

                for item in items['response']['items']:
                    collect_data = {}
                    created_at = datetime.datetime.fromtimestamp(item['date'])
                    if created_at >= datetime.datetime.now() - datetime.timedelta(minutes=15):
                        collect_data['id'] = item['id']
                        collect_data['created_at'] = str(created_at)
                        collect_data['text'] = item['text']
                        result.append(collect_data)
                    else:
                        has_next = False
                offset += 5
                print(result)
                print()

vk = Vkontakte()
vk.get_pub('wall.get', 'owner_id=568250150', vk.TOKEN_VK)
