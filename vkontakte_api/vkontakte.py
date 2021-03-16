import datetime

from vkontakte_api.config import BASE_URL, ID, TOKEN_VK
from vkontakte_api.services import RequestVkontakte, ParsePublication


class VkontaktePublication:
    """
    Класс публикаций Вконтакте
    """

    def __init__(self, request: RequestVkontakte, publications: ParsePublication):
        self.request = request
        self.publications = publications

    def get_publications(self, to_date=''):
        """Возвращает публикации со стены пользователя либо сообщества."""
        return self.publications.parse(to_date)


if __name__ == '__main__':
    request = RequestVkontakte(url=BASE_URL, id=ID, token=TOKEN_VK)
    parse = ParsePublication(request=request)
    vk = VkontaktePublication(request, parse)
    to_date = datetime.datetime(2020, 10, 10)
    print(vk.get_publications(to_date))

