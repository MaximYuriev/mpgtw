from src.dto.user import UserInfoToBrokerDTO, UpdateUserInfoDTO
from src.publisher.user import UserPublisher
from src.schemas.user import UserInfoToBrokerSchema, UpdateUserInfoToBrokerSchema


class UserBrokerAdapter:
    broker = UserPublisher

    @classmethod
    async def publish_create_user_info(cls, user_info: UserInfoToBrokerDTO) -> None:
        user_info_schema = UserInfoToBrokerSchema(
            user_id=user_info.id,
            firstname=user_info.firstname,
            lastname=user_info.lastname,
        )
        await cls.broker.publish_create_user_info(user_info_schema)

    @classmethod
    async def publish_update_user_info(cls, update_user_info: UpdateUserInfoDTO) -> None:
        update_user_info_schema = UpdateUserInfoToBrokerSchema(
            user_id=update_user_info.id,
            lastname=update_user_info.lastname,
            firstname=update_user_info.firstname,
        )
        await cls.broker.publish_update_user_info(update_user_info_schema)
