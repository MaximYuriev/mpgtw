from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response

from config import COOKIE_KEY_NAME
from ..exceptions.user import AuthException
from ..adapters.user import UserAdapter
from ..dependencies.user import get_user_adapter
from ..dependencies.auth import get_auth_service
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
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.message
        )
    else:
        response.set_cookie(COOKIE_KEY_NAME, value=access_token)
        return BaseResponse(detail="Вы успешно вошли в аккаунт!")