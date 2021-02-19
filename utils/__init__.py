from abc import ABC, abstractmethod


class RequestGet(ABC):
    """
    Базовый интерфейс запроса GET
    """

    @property
    @abstractmethod
    def base_url(self):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass


class ParseData(ABC):
    """
    Базовый интерфейс пасринга данных
    """

    @abstractmethod
    def parse(self, *args, **kwargs):
        pass
