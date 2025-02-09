from abc import ABC, abstractmethod

from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.sender import BaseHttpSender
from src.core.product.dto import ProductDTO, UpdateProductDTO, CreateProductDTO, ProductFilters


class BaseProductHttpSender(ABC, BaseHttpSender):
    _PRODUCT_SERVICE_URL = "http://localhost:8001"
    _CREATE_PRODUCT_URL = f"{_PRODUCT_SERVICE_URL}/product"
    _GET_PRODUCT_URL = f"{_PRODUCT_SERVICE_URL}/product"
    _UPDATE_PRODUCT_URL = f"{_PRODUCT_SERVICE_URL}/product"
    _DELETE_PRODUCT_URL = f"{_PRODUCT_SERVICE_URL}/product"

    @abstractmethod
    async def create_new_product(self, product: CreateProductDTO, cookie: CookieDTO) -> None:
        ...

    @abstractmethod
    async def get_products(self, filters: ProductFilters) -> list[ProductDTO]:
        ...

    @abstractmethod
    async def get_product(self, product_id: int) -> ProductDTO:
        ...

    @abstractmethod
    async def delete_product(self, product_id: int, cookie: CookieDTO) -> None:
        ...

    @abstractmethod
    async def update_product(self, product_id: int, update_product_data: UpdateProductDTO, cookie: CookieDTO) -> None:
        ...
