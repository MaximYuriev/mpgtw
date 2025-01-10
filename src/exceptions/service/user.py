from dataclasses import dataclass

from .base import ServiceException

@dataclass
class LoginIsNotUniqueException(ServiceException):
    @property
    def message(self):
        return "Логин не уникальный!"