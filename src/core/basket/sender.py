from aiohttp import ClientSession

from src.core.basket.dto import UpdateProductOnBasketDTO, AddProductOnBasketDTO, BasketDTO, ProductOnBasket
from src.core.basket.interfaces.sender import BaseBasketHttpSender
from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.exceptions.sender import HttpSenderRequestException


class BasketHttpSender(BaseBasketHttpSender):
    def __init__(self, session: ClientSession):
        self._session = session

    async def get_basket(self, cookie: CookieDTO) -> BasketDTO:
        response = await self._session.get(
            f'{self._GET_BASKET_URL}',
            cookies=((cookie.key, cookie.value),),
        )
        response_body = await response.json()
        basket_service_response = self._validate_responses(response_body)
        if response.status != 200:
            raise HttpSenderRequestException(response.status, basket_service_response.detail)
        return BasketDTO(
            basket_id=basket_service_response.data["basket_id"],
            products_on_basket=[ProductOnBasket(**product) for product in
                                basket_service_response.data["products_on_basket"]]
        )

    async def add_product_on_basket(self, added_product: AddProductOnBasketDTO, cookie: CookieDTO) -> None:
        response = await self._session.post(
            f'{self._ADD_PRODUCT_ON_BASKET_URL}',
            json=added_product.__dict__,
            cookies=((cookie.key, cookie.value),),
        )
        response_body = await response.json()
        basket_service_response = self._validate_responses(response_body)
        if response.status != 200:
            raise HttpSenderRequestException(response.status, basket_service_response.detail)

    async def update_product_on_basket(
            self,
            product_id: int,
            updated_product: UpdateProductOnBasketDTO,
            cookie: CookieDTO
    ) -> None:
        response = await self._session.patch(
            f'{self._UPDATE_PRODUCT_ON_BASKET_URL}/{product_id}',
            json=updated_product.__dict__,
            cookies=((cookie.key, cookie.value),),
        )
        response_body = await response.json()
        basket_service_response = self._validate_responses(response_body)
        if response.status != 200:
            raise HttpSenderRequestException(response.status, basket_service_response.detail)

    async def delete_product_from_basket(self, product_id: int, cookie: CookieDTO) -> None:
        response = await self._session.delete(
            f'{self._DELETE_PRODUCT_FROM_BASKET_URL}/{product_id}',
            cookies=((cookie.key, cookie.value),),
        )
        response_body = await response.json()
        basket_service_response = self._validate_responses(response_body)
        if response.status != 200:
            raise HttpSenderRequestException(response.status, basket_service_response.detail)
