from src.core.basket.dto import BasketDTO, AddProductOnBasketDTO, UpdateProductOnBasketDTO
from src.core.basket.interfaces.sender import BaseBasketHttpSender
from src.core.commons.dto.cookie import CookieDTO


class BasketService:
    def __init__(self, sender: BaseBasketHttpSender):
        self._sender = sender

    async def get_basket(self, cookie: CookieDTO) -> BasketDTO:
        return await self._sender.get_basket(cookie)

    async def add_product_on_basket(self, added_product: AddProductOnBasketDTO, cookie: CookieDTO) -> None:
        await self._sender.add_product_on_basket(added_product, cookie)

    async def update_product_on_basket(
            self,
            product_id: int,
            updated_product: UpdateProductOnBasketDTO,
            cookie: CookieDTO
    ) -> None:
        await self._sender.update_product_on_basket(product_id, updated_product, cookie)

    async def delete_product_from_basket(self, product_id: int, cookie: CookieDTO) -> None:
        await self._sender.delete_product_from_basket(product_id, cookie)
