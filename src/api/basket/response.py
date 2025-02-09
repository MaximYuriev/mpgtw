from src.api.basket.schemas import BasketSchema
from src.api.user.schemas.response import BaseResponse


class BasketResponse(BaseResponse):
    data: BasketSchema | None = None
