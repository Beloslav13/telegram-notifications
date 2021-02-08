import requests
from pprint import pprint
import os


class Vkontakte:
    TOKEN_VK = os.environ.get("TOKEN_VK", '')
    BASE_URL = 'https://api.vk.com/method/{}?{}&v=5.52&access_token={}'

    # 568250150
    def get_pub(self, method, id, token):
        resp = requests.get(self.BASE_URL.format(method, id, token)).json()
        print(resp)


vk = Vkontakte()
vk.get_pub('wall.get', 'owner_id=568250150', vk.TOKEN_VK)
