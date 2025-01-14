import uuid
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class RefreshTokenDTO:
    refresh_token: str
    user_id: uuid.UUID
