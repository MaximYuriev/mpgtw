import uuid

from src.core.commons.schemas.publish import PublishToBrokerSchema


class BasketBrokerSchema(PublishToBrokerSchema):
    basket_id: uuid.UUID


class CreateBasketBrokerSchema(BasketBrokerSchema):
    pass
