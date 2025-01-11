from dataclasses import dataclass

from .base import ServiceException


@dataclass
class LoginIsNotUniqueException(ServiceException):
    @property
    def message(self):
        return "Логин уже зарегистрирован в системе!"


@dataclass
class AuthException(ServiceException):
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
