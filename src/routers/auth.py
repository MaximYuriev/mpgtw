from typing import Annotated

from fastapi import APIRouter, Depends, Response

from config import COOKIE_KEY_NAME
from ..exceptions.application.user import AuthException
from ..exceptions.application.token import TokenInvalidException
from ..exceptions.http.auth import HTTPAuthException, HTTPTokenInvalidException
from ..adapters.user import UserAdapter
from ..dependencies.user import get_user_adapter
from ..dependencies.auth import get_auth_service, get_token_from_cookie
from ..services.auth import AuthService
from ..schemas.user import UserLoginSchema
from ..schemas.response import BaseResponse

auth_router = APIRouter(prefix="/auth", tags=['Auth'])


@auth_router.post("")
async def user_authenticate(
        user_login_schema: UserLoginSchema,
        user_adapter: Annotated[UserAdapter, Depends(get_user_adapter)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response
):
    try:
        user = await user_adapter.validate_user(user_login_schema)
        access_token = await auth_service.auth_user(user)
    except AuthException as exc:
        raise HTTPAuthException(exc.message)
    else:
        response.set_cookie(COOKIE_KEY_NAME, value=access_token)
        return BaseResponse(detail="Вы успешно вошли в аккаунт!")


@auth_router.get("/refresh")
async def refresh_access_token(
        access_token: Annotated[str, Depends(get_token_from_cookie)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        response: Response,
):
    try:
        access_token = await auth_service.refresh_access_token(access_token)
    except TokenInvalidException:
        raise HTTPTokenInvalidException()
    else:
        response.set_cookie(COOKIE_KEY_NAME, value=access_token)
        return BaseResponse(detail="Токен успешно обновлен!")
