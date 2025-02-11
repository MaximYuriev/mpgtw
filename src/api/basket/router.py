from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.basket.adapter import BasketServiceAdapter
from src.api.basket.filters import ProductOnBasketFilterSchema
from src.api.basket.response import BasketResponse
from src.api.basket.schemas import UpdateProductSchema, AddProductSchema
from src.api.user.dependencies.auth import get_auth_cookie
from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.exceptions.sender import HttpSenderRequestException

basket_router = APIRouter(prefix="/basket", tags=['Basket'])


@basket_router.get("")
@inject
async def get_basket(
        filters: Annotated[ProductOnBasketFilterSchema, Query()],
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        basket_adapter: FromDishka[BasketServiceAdapter]
):
    try:
        basket = await basket_adapter.get_basket(cookie, filters)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return BasketResponse(detail="Корзина найдена!", data=basket)


@basket_router.post("")
@inject
async def add_product_on_basket(
        add_product_schema: AddProductSchema,
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        basket_adapter: FromDishka[BasketServiceAdapter]
):
    try:
        await basket_adapter.add_product_on_basket(add_product_schema, cookie)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return BasketResponse(detail="Товар добавлен в корзину!")


@basket_router.patch("/{product_id}")
@inject
async def update_product_on_basket(
        product_id: int,
        update_product_schema: UpdateProductSchema,
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        basket_adapter: FromDishka[BasketServiceAdapter]
):
    try:
        await basket_adapter.update_product_on_basket(product_id, update_product_schema, cookie)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return BasketResponse(detail="Товар изменен в корзине!")


@basket_router.delete("/{product_id}")
@inject
async def update_product_on_basket(
        product_id: int,
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        basket_adapter: FromDishka[BasketServiceAdapter]
):
    try:
        await basket_adapter.delete_product_from_basket(product_id, cookie)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return BasketResponse(detail="Товар удален из корзины!")
