from aio_pika import RobustQueue
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from config import rabbit_url
from ..schemas.user import UserInfoToBrokerSchema


class UserPublisher:
    _EXCHANGE = RabbitExchange(
        name="user",
    )
    _QUEUE = RabbitQueue(
        name="user-info"
    )
    _ROUTING_KEY = "info"

    @classmethod
    async def _declare_exchange(cls, broker: RabbitBroker) -> None:
        await broker.declare_exchange(cls._EXCHANGE)

    @classmethod
    async def _declare_user_info_queue(cls, broker: RabbitBroker) -> None:
        queue = await broker.declare_queue(cls._QUEUE)
        await cls._bind_queue_to_exchange(queue)

    @classmethod
    async def _bind_queue_to_exchange(cls, queue: RobustQueue) -> None:
        await queue.bind(
            exchange=cls._EXCHANGE.name,
            routing_key="info"
        )

    @classmethod
    async def publish_user_info(cls, user_info: UserInfoToBrokerSchema) -> None:
        async with RabbitBroker(rabbit_url) as broker:
            await cls._declare_exchange(broker)
            await cls._declare_user_info_queue(broker)
            await broker.publish(
                message=user_info,
                exchange=cls._EXCHANGE,
                routing_key=cls._ROUTING_KEY
            )