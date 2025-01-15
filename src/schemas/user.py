import uuid
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    login: Annotated[str, MinLen(7), MaxLen(15)]
    password: Annotated[str, MinLen(8), MaxLen(20)]
    firstname: Annotated[str, MinLen(3), MaxLen(15)]
    lastname: Annotated[str, MinLen(3), MaxLen(15)]


class UserLoginSchema(BaseModel):
    login: str
    password: str


class UserInfoToBrokerSchema(BaseModel):
    user_id: uuid.UUID
    firstname: str
    lastname: str
