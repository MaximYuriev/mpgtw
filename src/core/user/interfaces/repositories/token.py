import uuid
from abc import ABC, abstractmethod

from src.core.user.dto.token import RefreshTokenDTO


class ITokenRepository(ABC):
    @abstractmethod
    async def save_token(self, token: RefreshTokenDTO) -> None:
        ...

    @abstractmethod
    async def get_token(self, user_id: uuid.UUID | str) -> RefreshTokenDTO:
        ...

    @abstractmethod
    async def delete_token(self, token: RefreshTokenDTO) -> None:
        ...
