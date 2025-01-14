from dataclasses import dataclass

from .base import ApplicationException


class TokenException(ApplicationException):
    pass


@dataclass
class TokenNotFoundException(TokenException):
   @property
   def message(self):
       return 'Токен не найден!'
