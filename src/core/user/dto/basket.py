import uuid
from dataclasses import dataclass


@dataclass
class CreateBasketDTO:
    basket_id: uuid.UUID
