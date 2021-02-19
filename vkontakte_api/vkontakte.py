from pprint import pprint

from vkontakte_api.config import BASE_URL, ID, TOKEN_VK
from vkontakte_api.services import RequestVkontakte, ParsePublication


class VkontaktePublication:
    """
    Класс публикаций Вконтакте
    """

    def __init__(self, id):
        self.id = id
        self.request = RequestVkontakte(url=BASE_URL, id=id, token=TOKEN_VK)
        self.publications = ParsePublication()


vk = VkontaktePublication(ID)
resp = vk.request.get()
pprint(vk.publications.parse(resp))
