from aio_pika import RobustQueue
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from src.core.commons.schemas.publish import PublishToBrokerSchema
from src.core.user.broker.schemas.basket import CreateBasketBrokerSchema
from src.core.user.broker.schemas.user import UserInfoToBrokerSchema, UpdateUserInfoToBrokerSchema


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

    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def _declare_exchange(self) -> None:
        await self._broker.declare_exchange(self._EXCHANGE)

    async def _declare_queue(self, queue: RabbitQueue) -> RobustQueue:
        queue = await self._broker.declare_queue(queue)
        await self._bind_queue_to_exchange(queue)
        return queue

    async def _bind_queue_to_exchange(self, queue: RobustQueue) -> None:
        await queue.bind(
            exchange=self._EXCHANGE.name,
            routing_key=queue.name,
        )

    async def _publish(self, queue: RobustQueue, user_info: PublishToBrokerSchema):
        await self._broker.publish(
            message=user_info,
            exchange=self._EXCHANGE,
            routing_key=queue.name,
        )

    async def publish_create_user_info(self, user_info: UserInfoToBrokerSchema) -> None:
        await self._declare_exchange()
        queue = await self._declare_queue(self._CREATE_USER_INFO_QUEUE)
        await self._publish(queue, user_info)

    async def publish_update_user_info(self, update_user_info: UpdateUserInfoToBrokerSchema) -> None:
        await self._declare_exchange()
        queue = await self._declare_queue(self._UPDATE_USER_INFO_QUEUE)
        await self._publish(queue, update_user_info)

    async def publish_create_basket(self, create_basket_schema: CreateBasketBrokerSchema) -> None:
        await self._declare_exchange()
        queue = await self._declare_queue(self._CREATE_USER_BASKET_QUEUE)
        await self._publish(queue, create_basket_schema)
