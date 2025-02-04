import uuid

from src.schemas.base import PublishToBrokerSchema


class BasketBrokerSchema(PublishToBrokerSchema):
    basket_id: uuid.UUID


class CreateBasketBrokerSchema(BasketBrokerSchema):
    pass
