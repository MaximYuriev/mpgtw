import bcrypt

from ..dto.user import UserLoginDTO
from ..exceptions.user import LoginIsNotUniqueException, LoginAuthException, PasswordAuthException
from ..repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

    async def _validate_login(self, login: str) -> None:
        user = await self._repository.get_user_by_login(login)
        if user is not None:
            raise LoginIsNotUniqueException

    @staticmethod
    def _validate_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @staticmethod
    def _hash_password(password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed_password.decode()

    async def create_user(self, user_login: UserLoginDTO) -> None:
        await self._validate_login(user_login.login)
        user_login.password = self._hash_password(user_login.password)
        await self._repository.save_into_db(user_login)

    async def validate_user(self, user_login: UserLoginDTO) -> None:
        founded_user = await self._repository.get_user_by_login(user_login.login)
        if founded_user is None:
            raise LoginAuthException
        if not self._validate_password(user_login.password, founded_user.password):
            raise PasswordAuthException
