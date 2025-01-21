import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from authorizer.http.dependencies import get_user_id_from_token
from ..adapters.user.service import UserAdapter
from ..dependencies.user import get_user_adapter
from ..dependencies.auth import get_auth_cookie
from ..dto.cookie import CookieDTO
from ..exceptions.application.user import LoginIsNotUniqueException
from ..exceptions.http.user import HTTPLoginIsNotUniqueException
from ..exceptions.http.sender import HttpSenderRequestException
from ..schemas.response import BaseResponse, UserResponse
from ..schemas.user import CreateUserSchema, EditUserInfoSchema, EditUserLoginSchema

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("")
async def create_user(
        create_user_schema: CreateUserSchema,
        user_adapter: Annotated[UserAdapter, Depends(get_user_adapter)],
):
    try:
        await user_adapter.create_user(create_user_schema)
    except LoginIsNotUniqueException as exc:
        raise HTTPLoginIsNotUniqueException(exc.message)
    else:
        return BaseResponse(detail="Пользователь успешно зарегистрирован!")


@user_router.get("")
async def get_user_info(
        cookie: Annotated[CookieDTO, Depends(get_auth_cookie)],
        user_adapter: Annotated[UserAdapter, Depends(get_user_adapter)],
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
async def edit_user_info(
        user_info_schema: EditUserInfoSchema,
        user_id: Annotated[uuid.UUID, Depends(get_user_id_from_token)],
        user_adapter: Annotated[UserAdapter, Depends(get_user_adapter)],
):
    await user_adapter.update_user_info(user_id, user_info_schema)
    return BaseResponse(detail="Данные в скором времени будут изменены!")


@user_router.patch("/edit/login")
async def edit_user_login(
        user_login_schema: EditUserLoginSchema,
        user_id: Annotated[uuid.UUID, Depends(get_user_id_from_token)],
        user_adapter: Annotated[UserAdapter, Depends(get_user_adapter)],
):
    try:
        await user_adapter.update_user_login(user_id, user_login_schema)
    except LoginIsNotUniqueException as exc:
        raise HTTPLoginIsNotUniqueException(exc.message)
    else:
        return BaseResponse(detail="Данные успешно изменены!")
