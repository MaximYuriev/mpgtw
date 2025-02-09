from src.api.product.schemas import ProductSchema
from src.api.user.schemas.response import BaseResponse


class ProductResponse(BaseResponse):
    data: ProductSchema | list[ProductSchema] | None = None
