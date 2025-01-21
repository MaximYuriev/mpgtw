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
    role: str


@dataclass
class UserLoginDTO(AbstractUserDTO):
    login: str
    password: str


@dataclass
class UserInfoDTO(AbstractUserDTO):
    firstname: str
    lastname: str


@dataclass
class UserInfoToBrokerDTO(UserInfoDTO):
    id: uuid.UUID


@dataclass
class UpdateUserInfoDTO(UserInfoDTO):
    id: uuid.UUID
    firstname: str | None
    lastname: str | None


@dataclass
class UpdateUserLoginDTO(UserLoginDTO):
    id: uuid.UUID
    login: str | None
    password: str | None
