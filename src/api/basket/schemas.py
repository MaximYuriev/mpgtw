import uuid

from pydantic import BaseModel, Field


class ProductOnBasketSchema(BaseModel):
    product_id: int
    product_name: str
    quantity_on_basket: int
    price_per_piece: int
    marked_for_order: bool


class AddProductSchema(BaseModel):
    product_id: int
    quantity_on_basket: int = Field(ge=1, le=20)
    marked_for_order: bool = Field(default=True)


class UpdateProductSchema(BaseModel):
    quantity_on_basket: int | None = Field(default=None, ge=1, le=20)
    marked_for_order: bool | None = None


class BasketSchema(BaseModel):
    basket_id: uuid.UUID
    products_on_basket: list[ProductOnBasketSchema]
