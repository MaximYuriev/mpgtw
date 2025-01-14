from .base import ApplicationException


class UserException(ApplicationException):
    pass


class LoginIsNotUniqueException(UserException):
    @property
    def message(self):
        return "Логин уже зарегистрирован в системе!"


class AuthException(UserException):
    @property
    def message(self):
        return "Неверный логин или пароль!"


class LoginAuthException(AuthException):
    pass


class PasswordAuthException(AuthException):
    pass
