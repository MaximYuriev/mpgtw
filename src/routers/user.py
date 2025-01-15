from typing import Annotated

from fastapi import APIRouter, Depends

from ..adapters.user.service import UserAdapter
from ..dependencies.user import get_user_adapter
from ..exceptions.application.user import LoginIsNotUniqueException
from ..exceptions.http.user import HTTPLoginIsNotUniqueException
from ..schemas.response import BaseResponse
from ..schemas.user import CreateUserSchema

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
