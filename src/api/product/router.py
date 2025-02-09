from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException, Depends, Query

from src.api.product.adapter import ProductServiceAdapter
from src.api.product.filters import PaginationQueryParamsWithCategory
from src.api.product.response import ProductResponse
from src.api.product.schemas import CreateProductSchema, UpdateProductSchema
from src.api.user.dependencies.auth import get_auth_cookie
from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.exceptions.sender import HttpSenderRequestException

product_router = APIRouter(prefix="/product", tags=['Product'])


@product_router.post("")
@inject
async def create_product(
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        create_product_schema: CreateProductSchema,
        product_adapter: FromDishka[ProductServiceAdapter],
):
    try:
        await product_adapter.create_product(create_product_schema, cookie)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return ProductResponse(detail="Товар успешно создан!")


@product_router.get("/{product_id}")
@inject
async def get_product_by_id(
        product_id: int,
        product_adapter: FromDishka[ProductServiceAdapter],
):
    try:
        product = await product_adapter.get_product_by_id(product_id)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return ProductResponse(detail="Товар найден!", data=product)


@product_router.get("")
@inject
async def get_product_list(
        pagination_params: Annotated[PaginationQueryParamsWithCategory, Query()],
        product_adapter: FromDishka[ProductServiceAdapter],
):
    products = await product_adapter.get_product_list(pagination_params)
    return ProductResponse(detail="Найденные товары:", data=products)


@product_router.patch("/{product_id}")
@inject
async def update_product(
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        product_id: int,
        update_product_schema: UpdateProductSchema,
        product_adapter: FromDishka[ProductServiceAdapter],
):
    try:
        await product_adapter.update_product(product_id, update_product_schema, cookie)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return ProductResponse(detail="Товар успешно удален!")


@product_router.delete("/{product_id}")
@inject
async def delete_product(
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        product_id: int,
        product_adapter: FromDishka[ProductServiceAdapter],
):
    try:
        await product_adapter.delete_product(product_id, cookie)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return ProductResponse(detail="Товар успешно удален!")
