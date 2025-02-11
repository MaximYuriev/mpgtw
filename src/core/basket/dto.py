import uuid
from dataclasses import dataclass


@dataclass
class ProductOnBasket:
    product_id: int
    product_name: str
    quantity_on_basket: int
    price_per_piece: int
    marked_for_order: bool


@dataclass
class BasketDTO:
    basket_id: uuid.UUID
    products_on_basket: list[ProductOnBasket]


@dataclass
class AddProductOnBasketDTO:
    product_id: int
    quantity_on_basket: int
    marked_for_order: bool


@dataclass
class UpdateProductOnBasketDTO:
    quantity_on_basket: int | None = None
    marked_for_order: bool | None = None


@dataclass
class ProductOnBasketFilter:
    with_products_marked_for_order: bool | None
