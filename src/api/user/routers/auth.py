from typing import Annotated

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Depends, Response

from authorizer.http.dependencies import get_token_from_cookie
from authorizer.http.exceptions import HTTPAuthException, HTTPTokenInvalidException
from authorizer.config import authorizer_config
from src.api.user.adapters.user import UserAdapter
from src.api.user.schemas.response import BaseResponse
from src.api.user.schemas.user import UserLoginSchema
from src.core.user.exceptions.token import TokenInvalidException
from src.core.user.exceptions.user import AuthException
from src.core.user.services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=['Auth'])


@auth_router.post("")
@inject
async def user_authenticate(
        user_login_schema: UserLoginSchema,
        user_adapter: FromDishka[UserAdapter],
        auth_service: FromDishka[AuthService],
        response: Response
):
    try:
        user = await user_adapter.validate_user(user_login_schema)
        access_token = await auth_service.auth_user(user)
    except AuthException as exc:
        raise HTTPAuthException(exc.message)
    else:
        response.set_cookie(authorizer_config.cookie.name, value=access_token)
        return BaseResponse(detail="Вы успешно вошли в аккаунт!")


@auth_router.get("/refresh")
@inject
async def refresh_access_token(
        access_token: Annotated[str, Depends(get_token_from_cookie)],
        auth_service: FromDishka[AuthService],
        response: Response,
):
    try:
        access_token = await auth_service.refresh_access_token(access_token)
    except TokenInvalidException:
        raise HTTPTokenInvalidException()
    else:
        response.set_cookie(authorizer_config.cookie.name, value=access_token)
        return BaseResponse(detail="Токен успешно обновлен!")
