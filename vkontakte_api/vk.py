import datetime
import time
import requests
from pprint import pprint
import os

from abc import ABC, abstractmethod


class BaseVkontakte(ABC):
    TOKEN_VK = os.environ.get("TOKEN_VK", 'ce5a37f2be02ca1c567cffdfec4dc2b4b9d8526ec313cf2aece578ea05b98d54c585c556c76a0c6942d69')
    BASE_URL = 'https://api.vk.com/method/{}?{}&v=5.52&access_token={}'
    TIME_OUT = 3

    def make_request(self, method, id, token, offset=0):
        """
        Выполнить get запрос к API Вконтакте.
        :param method: наименование метода к которому будет выполнен запрос (см. документацию Вк)
        :param id: owner_id либо domain
        :param token: access_token полученный при авторизации приложения
        :param offset: кол-во пропещенных публикаций
        :return: json из публикаций либо exceptions.ConnectionError
        """
        try_connection = 3
        while try_connection:
            try:
                # todo: universal get
                response = requests.get(self.BASE_URL.format(method, id, token), params={
                    "count": 10,
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

    @abstractmethod
    def get_last_publications(self, *args, **kwargs):
        pass


class PublicationWallVK(BaseVkontakte):
    """
    Класс публикаций на стене
    """

    # 568250150
    def get_last_publications(self, method, id, token):
        """
        Получить последнии публикации за последнии 15 минут.
        :return: список публикаций: [{item1}, {item2}, ..., ...,]
        """
        offset = 0
        has_next = True
        result = []
        while has_next:
            try:
                time.sleep(self.TIME_OUT)
                items = self.make_request(method, id, token, offset=offset)
            except requests.exceptions.ConnectionError as exc:
                print(f'Error: {exc}')
            else:
                # Отсекаем сразу ненужные публикации
                if not items['response']['items']:
                    break
                has_next, offset = self._parse_publications(has_next, items, offset, result)

    @staticmethod
    def _parse_publications(has_next, items, offset, result):
        for item in items['response']['items']:
            if 'is_pinned' in item or 'copy_history' in item:
                continue
            print(item)
            collect_data = {}
            created_at = datetime.datetime.fromtimestamp(item['date'])
            if created_at >= datetime.datetime.now() - datetime.timedelta(minutes=15):
                collect_data['id'] = item['id']
                collect_data['created_at'] = str(created_at)
                collect_data['text'] = item['text']
                result.append(collect_data)
            else:
                print('break')
                has_next = False
                break
        offset += 10
        print(result)
        print()
        return has_next, offset


vk = PublicationWallVK()
vk.get_last_publications('wall.get', 'owner_id=568250150', vk.TOKEN_VK)
