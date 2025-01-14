from .base import ApplicationException


class TokenException(ApplicationException):
    pass


class TokenNotFoundException(TokenException):
    @property
    def message(self):
        return 'Токен не найден!'
