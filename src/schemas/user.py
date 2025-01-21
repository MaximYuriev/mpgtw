import uuid
from abc import ABC
from typing import Annotated, Self

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, model_validator


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


class UpdateUserInfoToBrokerSchema(UserInfoToBrokerSchema):
    firstname: str | None = None
    lastname: str | None = None


class EditUserInfoSchema(UserInfoSchema):
    firstname: str | None = None
    lastname: str | None = None

    @model_validator(mode="after")
    def validate_not_empty_class(self) -> Self:
        if self.firstname is None and self.lastname is None:
            raise ValueError("Тело запроса не может быть пустым!")
        return self


class EditUserLoginSchema(UserLoginSchema):
    login: str | None = None
    password: str | None = None

    @model_validator(mode="after")
    def validate_not_empty_class(self) -> Self:
        if self.login is None and self.password is None:
            raise ValueError("Тело запроса не может быть пустым!")
        return self
