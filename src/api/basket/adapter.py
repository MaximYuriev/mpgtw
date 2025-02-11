from src.api.basket.filters import ProductOnBasketFilterSchema
from src.api.basket.schemas import BasketSchema, AddProductSchema, UpdateProductSchema
from src.core.basket.dto import AddProductOnBasketDTO, UpdateProductOnBasketDTO, ProductOnBasketFilter
from src.core.basket.service import BasketService
from src.core.commons.dto.cookie import CookieDTO


class BasketServiceAdapter:
    def __init__(self, service: BasketService):
        self._service = service

    async def get_basket(self, cookie: CookieDTO, filters: ProductOnBasketFilterSchema) -> BasketSchema:
        product_on_basket_filters = ProductOnBasketFilter(**filters.model_dump(by_alias=True))
        basket = await self._service.get_basket(cookie, product_on_basket_filters)
        return BasketSchema.model_validate(basket, from_attributes=True)

    async def add_product_on_basket(self, added_product_schema: AddProductSchema, cookie: CookieDTO) -> None:
        product = AddProductOnBasketDTO(**added_product_schema.model_dump())
        await self._service.add_product_on_basket(product, cookie)

    async def update_product_on_basket(
            self,
            product_id: int,
            updated_product_schema: UpdateProductSchema,
            cookie: CookieDTO,
    ) -> None:
        product = UpdateProductOnBasketDTO(**updated_product_schema.model_dump())
        await self._service.update_product_on_basket(product_id, product, cookie)

    async def delete_product_from_basket(self, product_id: int, cookie: CookieDTO) -> None:
        await self._service.delete_product_from_basket(product_id, cookie)
