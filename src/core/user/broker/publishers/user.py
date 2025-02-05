from aio_pika import RobustQueue, RobustExchange
from faststream.rabbit import RabbitBroker, RabbitExchange, RabbitQueue

from src.core.commons.schemas.publish import PublishToBrokerSchema
from src.core.user.broker.schemas.basket import CreateBasketBrokerSchema
from src.core.user.broker.schemas.user import UserInfoToBrokerSchema, UpdateUserInfoToBrokerSchema
from src.core.user.dto.basket import CreateBasketDTO
from src.core.user.dto.user import UserInfoToBrokerDTO, UpdateUserInfoDTO


class UserPublisher:
    _EXCHANGE_NAME = "user"

    _CREATE_USER_INFO_QUEUE_NAME = "user-info-create"

    _UPDATE_USER_INFO_QUEUE_NAME = "user-info-update"

    _CREATE_USER_BASKET_QUEUE_NAME = "basket-create"

    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def publish_create_user_info(self, user_info: UserInfoToBrokerDTO) -> None:
        exchange, queue = await self._prepare_to_publish(self._CREATE_USER_INFO_QUEUE_NAME)
        user_info_schema = UserInfoToBrokerSchema.model_validate(user_info, from_attributes=True)
        await self._publish(exchange, queue, user_info_schema)

    async def publish_update_user_info(self, update_user_info: UpdateUserInfoDTO) -> None:
        exchange, queue = await self._prepare_to_publish(self._UPDATE_USER_INFO_QUEUE_NAME)
        user_info_schema = UpdateUserInfoToBrokerSchema.model_validate(update_user_info, from_attributes=True)
        await self._publish(exchange, queue, user_info_schema)

    async def publish_create_basket(self, create_basket: CreateBasketDTO) -> None:
        exchange, queue = await self._prepare_to_publish(self._CREATE_USER_BASKET_QUEUE_NAME)
        basket_schema = CreateBasketBrokerSchema.model_validate(create_basket, from_attributes=True)
        await self._publish(exchange, queue, basket_schema)

    async def _prepare_to_publish(self, queue_name: str) -> tuple[RobustExchange, RobustQueue]:
        exchange = await self._declare_exchange()
        queue = await self._declare_queue(queue_name)
        await self._bind_queue_to_exchange(exchange, queue)
        return exchange, queue

    async def _publish(
            self,
            exchange: RobustExchange,
            queue: RobustQueue,
            product_schema: PublishToBrokerSchema,
    ) -> None:
        await self._broker.publish(
            message=product_schema,
            exchange=exchange.name,
            routing_key=queue.name,
        )

    async def _declare_exchange(self) -> RobustExchange:
        exchange = RabbitExchange(self._EXCHANGE_NAME)
        return await self._broker.declare_exchange(exchange)

    async def _declare_queue(self, queue_name: str) -> RobustQueue:
        rabbit_queue = RabbitQueue(queue_name)
        queue = await self._broker.declare_queue(rabbit_queue)
        return queue

    @staticmethod
    async def _bind_queue_to_exchange(exchange: RobustExchange, queue: RobustQueue) -> None:
        await queue.bind(
            exchange=exchange.name,
            routing_key=queue.name,
        )
