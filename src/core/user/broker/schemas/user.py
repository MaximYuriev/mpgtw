import uuid

from pydantic import Field

from src.core.commons.schemas.publish import PublishToBrokerSchema


class UserInfoToBrokerSchema(PublishToBrokerSchema):
    user_id: uuid.UUID = Field(validation_alias="id")
    firstname: str
    lastname: str


class UpdateUserInfoToBrokerSchema(UserInfoToBrokerSchema):
    firstname: str | None = None
    lastname: str | None = None
