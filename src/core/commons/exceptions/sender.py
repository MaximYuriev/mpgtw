from dataclasses import dataclass

from src.core.commons.exceptions.base import ApplicationException


class HttpSenderException(ApplicationException):
    pass


@dataclass
class HttpSenderRequestException(HttpSenderException):
    _status: int
    _msg: str

    @property
    def status_code(self):
        return self._status

    @property
    def detail(self):
        return self._msg


class HttpSenderValidateException(HttpSenderException):
    @property
    def message(self):
        return "Ошибка валидации!"
