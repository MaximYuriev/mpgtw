from src.core.commons.exceptions.base import ApplicationException


class TokenInvalidException(ApplicationException):
    @property
    def message(self):
        return "Токен недействительный!"


class TokenNotFoundException(TokenInvalidException):
    @property
    def message(self):
        return 'Токен не найден!'


class TokenExpiredException(TokenInvalidException):
    @property
    def message(self):
        return "Время жизни токена истекло!"
