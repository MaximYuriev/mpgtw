import uuid

from src.core.commons.schemas.publish import PublishToBrokerSchema


class UserInfoToBrokerSchema(PublishToBrokerSchema):
    user_id: uuid.UUID
    firstname: str
    lastname: str


class UpdateUserInfoToBrokerSchema(UserInfoToBrokerSchema):
    firstname: str | None = None
    lastname: str | None = None
