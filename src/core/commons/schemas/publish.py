from abc import ABC

from pydantic import BaseModel


class PublishToBrokerSchema(BaseModel, ABC):
    pass
