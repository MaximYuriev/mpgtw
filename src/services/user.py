import bcrypt

from ..adapters.user.broker import UserBrokerAdapter
from ..dto.user import UserLoginDTO, UserDTO, UserInfoDTO, UserInfoToBrokerDTO
from ..exceptions.application.user import LoginIsNotUniqueException, LoginAuthException, PasswordAuthException
from ..repositories.user import UserRepository


class UserService:
    broker_adapter = UserBrokerAdapter

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

    async def _publish_user_info(self, user_info: UserInfoToBrokerDTO) -> None:
        await self.broker_adapter.publish(user_info)

    async def create_user(self, user_login: UserLoginDTO, user_info: UserInfoDTO) -> None:
        await self._validate_login(user_login.login)
        user_login.password = self._hash_password(user_login.password)
        user_id = await self._repository.save_into_db(user_login)
        user_info_to_broker = UserInfoToBrokerDTO(
            firstname=user_info.firstname,
            lastname=user_info.lastname,
            id = user_id
        )
        await self._publish_user_info(user_info_to_broker)

    async def validate_user(self, user_login: UserLoginDTO) -> UserDTO:
        founded_user = await self._repository.get_user_by_login(user_login.login)
        if founded_user is None:
            raise LoginAuthException
        if not self._validate_password(user_login.password, founded_user.password):
            raise PasswordAuthException
        return founded_user
