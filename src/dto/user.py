from abc import ABC
from dataclasses import dataclass


class UserDTO(ABC):
    pass


@dataclass
class UserLoginDTO(UserDTO):
    login: str
    password: str


@dataclass
class UserInfoDTO(UserDTO):
    firstname: str
    lastname: str


@dataclass
class UserPayloadDTO(UserDTO):
    sub: str
    role: str
