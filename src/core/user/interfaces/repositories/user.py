import uuid
from abc import ABC, abstractmethod

from src.core.user.dto.user import UserLoginDTO, UserDTO, UpdateUserLoginDTO


class IUserRepository(ABC):
    @abstractmethod
    async def save_into_db(self, user_login: UserLoginDTO) -> uuid.UUID:
        ...

    @abstractmethod
    async def get_user_by_login(self, login: str) -> UserDTO | None:
        ...

    @abstractmethod
    async def update_user(self, updated_user_login: UpdateUserLoginDTO) -> None:
        ...
