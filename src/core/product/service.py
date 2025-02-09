from src.core.commons.dto.cookie import CookieDTO
from src.core.product.dto import ProductDTO, CreateProductDTO, UpdateProductDTO, ProductFilters
from src.core.product.interfaces.sender import BaseProductHttpSender


class ProductService:
    def __init__(self, sender: BaseProductHttpSender):
        self._sender = sender

    async def create_new_product(self, product: CreateProductDTO, cookie: CookieDTO) -> None:
        await self._sender.create_new_product(product, cookie)

    async def get_product_list(self, filters: ProductFilters) -> list[ProductDTO]:
        return await self._sender.get_products(filters)

    async def get_product_by_id(self, product_id: int) -> ProductDTO:
        return await self._sender.get_product(product_id)

    async def delete_product(self, product_id: int, cookie: CookieDTO) -> None:
        await self._sender.delete_product(product_id, cookie)

    async def update_product(self, product_id: int, update_product: UpdateProductDTO, cookie: CookieDTO) -> None:
        await self._sender.update_product(product_id, update_product, cookie)
