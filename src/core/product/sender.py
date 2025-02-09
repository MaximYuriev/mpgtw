from aiohttp import ClientSession

from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.exceptions.sender import HttpSenderRequestException
from src.core.product.dto import UpdateProductDTO, ProductDTO, CreateProductDTO, ProductFilters
from src.core.product.interfaces.sender import BaseProductHttpSender


class ProductHttpSender(BaseProductHttpSender):
    def __init__(self, session: ClientSession):
        self._session = session

    async def create_new_product(self, product: CreateProductDTO, cookie: CookieDTO) -> None:
        response = await self._session.post(
            f'{self._CREATE_PRODUCT_URL}',
            json=product.__dict__,
            cookies=((cookie.key, cookie.value),)
        )
        response_body = await response.json()
        product_service_response = self._validate_responses(response_body)
        if response.status != 200:
            raise HttpSenderRequestException(response.status, product_service_response.detail)

    async def get_products(self, filters: ProductFilters) -> list[ProductDTO]:
        query_parameters = filters.__dict__ if filters.category is not None else {"pn": filters.pn, "ps": filters.ps}
        response = await self._session.get(
            f'{self._GET_PRODUCT_URL}',
            params=query_parameters,
        )
        response_body = await response.json()
        product_service_response = self._validate_responses(response_body)
        if response.status != 200:
            raise HttpSenderRequestException(response.status, product_service_response.detail)
        return [ProductDTO(**product) for product in product_service_response.data]

    async def get_product(self, product_id: int) -> ProductDTO:
        response = await self._session.get(
            f'{self._GET_PRODUCT_URL}/{product_id}',
        )
        response_body = await response.json()
        product_service_response = self._validate_responses(response_body)
        if response.status == 200:
            return ProductDTO(**product_service_response.data)
        raise HttpSenderRequestException(response.status, product_service_response.detail)

    async def delete_product(self, product_id: int, cookie: CookieDTO) -> None:
        response = await self._session.delete(
            f'{self._DELETE_PRODUCT_URL}/{product_id}',
            cookies=((cookie.key, cookie.value),)
        )
        response_body = await response.json()
        product_service_response = self._validate_responses(response_body)
        if response.status != 200:
            raise HttpSenderRequestException(response.status, product_service_response.detail)

    async def update_product(self, product_id: int, update_product_data: UpdateProductDTO, cookie: CookieDTO) -> None:
        response = await self._session.patch(
            f'{self._UPDATE_PRODUCT_URL}/{product_id}',
            json=update_product_data.__dict__,
            cookies=((cookie.key, cookie.value),)
        )
        response_body = await response.json()
        product_service_response = self._validate_responses(response_body)
        if response.status != 200:
            raise HttpSenderRequestException(response.status, product_service_response.detail)
