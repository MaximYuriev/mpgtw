import uuid
from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Depends, HTTPException

from authorizer.http.dependencies import get_user_id_from_token
from src.api.user.adapters.user import UserAdapter
from src.api.user.dependencies.auth import get_auth_cookie
from src.api.user.exceptions.user import HTTPLoginIsNotUniqueException
from src.api.user.schemas.response import BaseResponse, UserResponse
from src.api.user.schemas.user import CreateUserSchema, EditUserInfoSchema, EditUserLoginSchema
from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.exceptions.sender import HttpSenderRequestException
from src.core.user.exceptions.user import LoginIsNotUniqueException

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("")
@inject
async def create_user(
        create_user_schema: CreateUserSchema,
        user_adapter: FromDishka[UserAdapter],
):
    try:
        await user_adapter.create_user(create_user_schema)
    except LoginIsNotUniqueException as exc:
        raise HTTPLoginIsNotUniqueException(exc.message)
    else:
        return BaseResponse(detail="Пользователь успешно зарегистрирован!")


@user_router.get("")
@inject
async def get_user_info(
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        user_adapter: FromDishka[UserAdapter],
):
    try:
        user_info = await user_adapter.get_user_info(cookie)
    except HttpSenderRequestException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.detail
        )
    else:
        return UserResponse(detail="Пользовательские данные:", data=user_info)


@user_router.patch("/edit/info")
@inject
async def edit_user_info(
        user_info_schema: EditUserInfoSchema,
        user_id: Annotated[uuid.UUID, Depends(get_user_id_from_token)],
        user_adapter: FromDishka[UserAdapter],
):
    await user_adapter.update_user_info(user_id, user_info_schema)
    return BaseResponse(detail="Данные в скором времени будут изменены!")


@user_router.patch("/edit/login")
@inject
async def edit_user_login(
        user_login_schema: EditUserLoginSchema,
        user_id: Annotated[uuid.UUID, Depends(get_user_id_from_token)],
        user_adapter: FromDishka[UserAdapter],
):
    try:
        await user_adapter.update_user_login(user_id, user_login_schema)
    except LoginIsNotUniqueException as exc:
        raise HTTPLoginIsNotUniqueException(exc.message)
    else:
        return BaseResponse(detail="Данные успешно изменены!")
