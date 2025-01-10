from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from ..adapters.user import UserAdapter
from ..dependencies.user import get_user_adapter
from ..exceptions.service.user import LoginIsNotUniqueException
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message
        )
    else:
        return BaseResponse(detail="Пользователь успешно зарегистрирован!")
