from aio_pika import RobustQueue
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from config import rabbit_url
from ..schemas.base import PublishToBrokerSchema
from ..schemas.basket import CreateBasketBrokerSchema
from ..schemas.user import UserInfoToBrokerSchema, UpdateUserInfoToBrokerSchema


class UserPublisher:
    _EXCHANGE = RabbitExchange(
        name="user"
    )
    _CREATE_USER_INFO_QUEUE = RabbitQueue(
        name="user-info-create"
    )
    _UPDATE_USER_INFO_QUEUE = RabbitQueue(
        name="user-info-update"
    )
    _CREATE_USER_BASKET_QUEUE = RabbitQueue(
        name="basket-create"
    )

    @classmethod
    async def _declare_exchange(cls, broker: RabbitBroker) -> None:
        await broker.declare_exchange(cls._EXCHANGE)

    @classmethod
    async def _declare_queue(cls, broker: RabbitBroker, queue: RabbitQueue) -> RobustQueue:
        queue = await broker.declare_queue(queue)
        await cls._bind_queue_to_exchange(queue)
        return queue

    @classmethod
    async def _bind_queue_to_exchange(cls, queue: RobustQueue) -> None:
        await queue.bind(
            exchange=cls._EXCHANGE.name,
            routing_key=queue.name,
        )

    @classmethod
    async def _publish(cls, broker: RabbitBroker, queue: RobustQueue, user_info: PublishToBrokerSchema):
        await broker.publish(
            message=user_info,
            exchange=cls._EXCHANGE,
            routing_key=queue.name,
        )

    @classmethod
    async def publish_create_user_info(cls, user_info: UserInfoToBrokerSchema) -> None:
        async with RabbitBroker(rabbit_url) as broker:
            await cls._declare_exchange(broker)
            queue = await cls._declare_queue(broker, cls._CREATE_USER_INFO_QUEUE)
            await cls._publish(broker, queue, user_info)

    @classmethod
    async def publish_update_user_info(cls, update_user_info: UpdateUserInfoToBrokerSchema) -> None:
        async with RabbitBroker(rabbit_url) as broker:
            await cls._declare_exchange(broker)
            queue = await cls._declare_queue(broker, cls._UPDATE_USER_INFO_QUEUE)
            await cls._publish(broker, queue, update_user_info)

    @classmethod
    async def publish_create_basket(cls, create_basket_schema: CreateBasketBrokerSchema) -> None:
        async with RabbitBroker(rabbit_url) as broker:
            await cls._declare_exchange(broker)
            queue = await cls._declare_queue(broker, cls._CREATE_USER_BASKET_QUEUE)
            await cls._publish(broker, queue, create_basket_schema)
