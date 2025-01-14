from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import async_session
from ..repositories.token import TokenRepository
from ..services.auth import AuthService


def get_token_repository(
        session: Annotated[AsyncSession, Depends(async_session)],
) -> TokenRepository:
    return TokenRepository(session)


def get_auth_service(
        token_repository: Annotated[TokenRepository, Depends(get_token_repository)],
) -> AuthService:
    return AuthService(token_repository)
