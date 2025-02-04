from src.schemas.basket import CreateBasketBrokerSchema
from src.dto.basket import CreateBasketDTO
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

    @classmethod
    async def publish_create_basket(cls, create_basket: CreateBasketDTO) -> None:
        create_basket_schema = CreateBasketBrokerSchema(basket_id=create_basket.basket_id)
        await cls.broker.publish_create_basket(create_basket_schema)
