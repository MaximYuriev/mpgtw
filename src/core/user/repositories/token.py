import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.user.dto.token import RefreshTokenDTO
from src.core.user.exceptions.token import TokenNotFoundException
from src.core.user.interfaces.repositories.token import ITokenRepository
from src.core.user.models.token import RefreshTokenModel


class TokenRepository(ITokenRepository):
    model = RefreshTokenModel

    def __init__(self, session: AsyncSession):
        self._session = session

    def _dto_to_model(self, token: RefreshTokenDTO) -> model:
        return self.model(
            refresh_token=token.refresh_token,
            user_id=token.user_id,
        )

    async def _get_token_model(self, **kwargs) -> model:
        query = select(RefreshTokenModel).filter_by(**kwargs)
        refresh_token_model = await self._session.scalar(query)
        if refresh_token_model is not None:
            return refresh_token_model
        raise TokenNotFoundException

    async def save_token(self, token: RefreshTokenDTO) -> None:
        refresh_token_model = self._dto_to_model(token)
        self._session.add(refresh_token_model)
        await self._session.commit()

    async def get_token(self, user_id: uuid.UUID | str) -> RefreshTokenDTO:
        refresh_token_model = await self._get_token_model(user_id=user_id)
        return RefreshTokenDTO(
            refresh_token=refresh_token_model.refresh_token,
            user_id=refresh_token_model.user_id,
        )

    async def delete_token(self, token: RefreshTokenDTO) -> None:
        refresh_token_model = await self._get_token_model(refresh_token=token.refresh_token)
        await self._session.delete(refresh_token_model)
        await self._session.commit()
