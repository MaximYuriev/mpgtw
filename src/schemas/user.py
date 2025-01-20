import uuid
from abc import ABC
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class BaseUserSchema(BaseModel, ABC):
    pass


class CreateUserSchema(BaseUserSchema):
    login: Annotated[str, MinLen(7), MaxLen(15)]
    password: Annotated[str, MinLen(8), MaxLen(20)]
    firstname: Annotated[str, MinLen(3), MaxLen(15)]
    lastname: Annotated[str, MinLen(3), MaxLen(15)]


class UserLoginSchema(BaseUserSchema):
    login: str
    password: str


class UserInfoSchema(BaseUserSchema):
    firstname: str
    lastname: str


class UserInfoToBrokerSchema(BaseUserSchema):
    user_id: uuid.UUID
    firstname: str
    lastname: str
