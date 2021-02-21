import datetime
import time
from typing import Dict

import requests

from utils import RequestGet, ParseData
from vkontakte_api.config import BASE_URL, TOKEN_VK, TIME_OUT


class RequestVkontakte(RequestGet):
    """
    Реализация базового интерфейса запроса GET
    """

    def __init__(self, url: str, id: str, token: str):
        self._url = url
        self.id = id
        self.token = token

    @property
    def base_url(self):
        """
        Базовый url к которому будет выполнен запрос.
        """
        return self._url

    def get(self, method='wall.get', offset=0):
        """
        Выполнить get запрос к API Вконтакте.
        :param method: наименование метода к которому будет выполнен запрос (см. документацию Вк)
        :param offset: кол-во пропещенных публикаций
        :return: json из публикаций либо exceptions.ConnectionError
        """

        try_connection = 3
        while try_connection:
            try:
                # todo: universal get
                response = requests.get(self.base_url.format(method, self.id, self.token), params={
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
            raise requests.exceptions.ConnectionError(
                f'Max retries exceeded with url: {self.base_url.format(method, self.id, self.token)}')


class ParsePublication(ParseData):
    """
    Реализация базового интерфейса парсинга данных Вконтакте
    """

    def __init__(self, request: RequestVkontakte):
        self.request = request

    def parse(self, to_date=None):
        """
        Парсим данные полученные по get запросу.
        Если to_date не передан будет спарсены публикации за последнии 15 минут.
        Если to_date передан, парсинг будет продолжаться до указанной даты.
        :param to_date: datetime.datetime
        :return: [{pub1: 1}, {pub2}: 2, ..., ...]
        """
        if to_date is None:
            to_date = datetime.datetime.now() - datetime.timedelta(minutes=15)

        offset = 0
        has_next = True
        result = []
        while has_next:
            try:
                time.sleep(TIME_OUT)
                items = self.request.get(offset=offset)
            except requests.exceptions.ConnectionError as exc:
                print(f'Error: {exc}')
            else:
                # Отсекаем сразу ненужные публикации
                if not items['response']['items']:
                    break
                for item in items['response']['items']:
                    if 'is_pinned' in item or 'copy_history' in item:
                        continue
                    collect_data = {}
                    created_at = datetime.datetime.fromtimestamp(item['date'])
                    if created_at >= to_date:
                        collect_data['id'] = item['id']
                        collect_data['created_at'] = str(created_at)
                        print(created_at)
                        collect_data['text'] = item['text']
                        result.append(collect_data)
                    else:
                        print('break')
                        has_next = False
                        break
                offset += 10
        return result
