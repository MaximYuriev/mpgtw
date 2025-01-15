from src.dto.user import UserInfoToBrokerDTO
from src.publisher.user import UserPublisher
from src.schemas.user import UserInfoToBrokerSchema


class UserBrokerAdapter:
    broker = UserPublisher

    @classmethod
    async def publish(cls, user_info: UserInfoToBrokerDTO) -> None:
        user_info_schema = UserInfoToBrokerSchema(
            user_id=user_info.id,
            firstname=user_info.firstname,
            lastname=user_info.lastname,
        )
        await cls.broker.publish_user_info(user_info_schema)
