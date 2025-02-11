from abc import ABC, abstractmethod

from src.core.basket.dto import BasketDTO, AddProductOnBasketDTO, UpdateProductOnBasketDTO, ProductOnBasketFilter
from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.sender import BaseHttpSender


class BaseBasketHttpSender(BaseHttpSender, ABC):
    _BASKET_SERVICE_URL = "http://localhost:8002"
    _GET_BASKET_URL = f'{_BASKET_SERVICE_URL}/basket'
    _ADD_PRODUCT_ON_BASKET_URL = f'{_BASKET_SERVICE_URL}/basket'
    _UPDATE_PRODUCT_ON_BASKET_URL = f'{_BASKET_SERVICE_URL}/basket'
    _DELETE_PRODUCT_FROM_BASKET_URL = f'{_BASKET_SERVICE_URL}/basket'

    @abstractmethod
    async def get_basket(self, cookie: CookieDTO, filters: ProductOnBasketFilter) -> BasketDTO:
        ...

    @abstractmethod
    async def add_product_on_basket(self, added_product: AddProductOnBasketDTO, cookie: CookieDTO) -> None:
        ...

    @abstractmethod
    async def update_product_on_basket(
            self,
            product_id: int,
            updated_product: UpdateProductOnBasketDTO,
            cookie: CookieDTO,
    ) -> None:
        ...

    @abstractmethod
    async def delete_product_from_basket(self, product_id: int, cookie: CookieDTO) -> None:
        ...
