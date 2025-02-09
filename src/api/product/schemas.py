from pydantic import BaseModel

from src.api.product.utils.category import Category


class BaseProductSchema(BaseModel):
    name: str
    category: Category
    quantity: int
    price: int


class ProductSchema(BaseProductSchema):
    product_id: int


class CreateProductSchema(BaseProductSchema):
    pass


class UpdateProductSchema(BaseProductSchema):
    name: str | None = None
    category: Category | None = None
    quantity: int | None = None
    price: int | None = None
