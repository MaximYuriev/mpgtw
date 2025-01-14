from dataclasses import dataclass


@dataclass
class AuthTokenInvalidException(Exception):
    @property
    def message(self):
        return "Токен недействительный!"


@dataclass
class AuthTokenExpiredException(AuthTokenInvalidException):
    @property
    def message(self):
        return "Время жизни токена истекло!"
