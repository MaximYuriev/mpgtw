from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from authorizer.http.dependencies import get_token_from_cookie
from config import async_session, COOKIE_KEY_NAME
from ..dto.cookie import CookieDTO
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


def get_auth_cookie(
        token: Annotated[str, Depends(get_token_from_cookie)]
) -> CookieDTO:
    return CookieDTO(
        key=COOKIE_KEY_NAME,
        value=token
    )
