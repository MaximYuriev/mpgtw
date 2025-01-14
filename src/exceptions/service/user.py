from dataclasses import dataclass

from .base import ServiceException


class UserException(ServiceException):
    pass


@dataclass
class LoginIsNotUniqueException(UserException):
    @property
    def message(self):
        return "Логин уже зарегистрирован в системе!"


@dataclass
class AuthException(UserException):
    @property
    def message(self):
        return "Неверный логин или пароль!"


@dataclass
class LoginAuthException(AuthException):
    @property
    def message(self):
        return "Неверный логин!"


@dataclass
class PasswordAuthException(AuthException):
    @property
    def message(self):
        return "Неверный пароль!"
