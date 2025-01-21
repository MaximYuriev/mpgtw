from aio_pika import RobustQueue
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from config import rabbit_url
from ..schemas.user import UserInfoToBrokerSchema, UpdateUserInfoToBrokerSchema


class UserPublisher:
    _EXCHANGE = RabbitExchange(
        name="user",
    )
    _CREATE_USER_INFO_QUEUE = RabbitQueue(
        name="user-info-create"
    )
    _UPDATE_USER_INFO_QUEUE = RabbitQueue(
        name="user-info-update"
    )
    _ROUTING_KEY = "info"

    @classmethod
    async def _declare_exchange(cls, broker: RabbitBroker) -> None:
        await broker.declare_exchange(cls._EXCHANGE)

    @classmethod
    async def _declare_queue(cls, broker: RabbitBroker, queue: RabbitQueue) -> None:
        queue = await broker.declare_queue(queue)
        await cls._bind_queue_to_exchange(queue)

    @classmethod
    async def _bind_queue_to_exchange(cls, queue: RobustQueue) -> None:
        await queue.bind(
            exchange=cls._EXCHANGE.name,
            routing_key=cls._ROUTING_KEY
        )

    @classmethod
    async def _publish(cls, broker: RabbitBroker, user_info: UserInfoToBrokerSchema):
        await broker.publish(
            message=user_info,
            exchange=cls._EXCHANGE,
            routing_key=cls._ROUTING_KEY
        )

    @classmethod
    async def publish_create_user_info(cls, user_info: UserInfoToBrokerSchema) -> None:
        async with RabbitBroker(rabbit_url) as broker:
            await cls._declare_exchange(broker)
            await cls._declare_queue(broker, cls._CREATE_USER_INFO_QUEUE)
            await cls._publish(broker, user_info)

    @classmethod
    async def publish_update_user_info(cls, update_user_info: UpdateUserInfoToBrokerSchema) -> None:
        async with RabbitBroker(rabbit_url) as broker:
            await cls._declare_exchange(broker)
            await cls._declare_queue(broker, cls._UPDATE_USER_INFO_QUEUE)
            await cls._publish(broker, update_user_info)
