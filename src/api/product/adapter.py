from src.api.product.filters import PaginationQueryParamsWithCategory
from src.api.product.schemas import ProductSchema, CreateProductSchema, UpdateProductSchema
from src.core.commons.dto.cookie import CookieDTO
from src.core.product.dto import CreateProductDTO, UpdateProductDTO, ProductFilters
from src.core.product.service import ProductService


class ProductServiceAdapter:
    def __init__(self, service: ProductService):
        self._service = service

    async def get_product_list(self, pagination_params: PaginationQueryParamsWithCategory) -> list[ProductSchema]:
        filters = ProductFilters(**pagination_params.model_dump())
        product_list = await self._service.get_product_list(filters)
        return [ProductSchema.model_validate(product, from_attributes=True) for product in product_list]

    async def get_product_by_id(self, product_id: int) -> ProductSchema:
        product = await self._service.get_product_by_id(product_id)
        return ProductSchema.model_validate(product, from_attributes=True)

    async def create_product(self, create_product_schema: CreateProductSchema, cookie: CookieDTO) -> None:
        product = CreateProductDTO(**create_product_schema.model_dump())
        await self._service.create_new_product(product, cookie)

    async def update_product(
            self,
            product_id: int,
            update_product_schema: UpdateProductSchema,
            cookie: CookieDTO,
    ) -> None:
        product = UpdateProductDTO(**update_product_schema.model_dump())
        await self._service.update_product(product_id, product, cookie)

    async def delete_product(self, product_id: int, cookie: CookieDTO) -> None:
        await self._service.delete_product(product_id, cookie)
