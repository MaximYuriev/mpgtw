import uuid
from abc import ABC
from dataclasses import dataclass


class AbstractUserDTO(ABC):
    pass


@dataclass
class UserDTO(AbstractUserDTO):
    id: uuid.UUID
    login: str
    password: str
    role: str | None = None


@dataclass
class UserLoginDTO(AbstractUserDTO):
    login: str
    password: str


@dataclass
class UserInfoDTO(AbstractUserDTO):
    firstname: str
    lastname: str
