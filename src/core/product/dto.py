from abc import ABC
from dataclasses import dataclass


@dataclass
class BaseProductDTO(ABC):
    name: str
    category: str
    quantity: int
    price: int


@dataclass
class ProductDTO(BaseProductDTO):
    product_id: int


@dataclass
class CreateProductDTO(BaseProductDTO):
    pass


@dataclass
class UpdateProductDTO(BaseProductDTO):
    name: str | None = None
    category: str | None = None
    quantity: int | None = None
    price: int | None = None


@dataclass
class ProductFilters:
    pn: int
    ps: int
    category: str | None = None
