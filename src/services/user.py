import bcrypt

from ..domains.user import UserLogin
from ..exceptions.service.user import LoginIsNotUniqueException
from ..repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def _validate_login(self, login: str) -> None:
        user = await self._repository.get_user_login(login)
        if user is not None:
            raise LoginIsNotUniqueException

    @staticmethod
    def _hash_password(password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed_password.decode()

    async def create_user(self, user_login: UserLogin) -> None:
        await self._validate_login(user_login.login)
        user_login.password = self._hash_password(user_login.password)
        await self._repository.save_into_db(user_login)
