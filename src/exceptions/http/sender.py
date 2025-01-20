from dataclasses import dataclass


class HttpSenderException(Exception):
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
