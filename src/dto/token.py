import uuid
from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class TokenDTO(ABC):
    pass


@dataclass(frozen=True, eq=False)
class RefreshTokenDTO(TokenDTO):
    refresh_token: str
    user_id: uuid.UUID
