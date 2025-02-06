import bcrypt

from src.core.commons.dto.cookie import CookieDTO
from src.core.user.dto.basket import CreateBasketDTO
from src.core.user.dto.user import UserLoginDTO, UserDTO, UserInfoDTO, UserInfoToBrokerDTO, UpdateUserInfoDTO, \
    UpdateUserLoginDTO
from src.core.user.exceptions.user import LoginIsNotUniqueException, LoginAuthException, PasswordAuthException
from src.core.user.interfaces.publishers.user import IUserPublisher
from src.core.user.interfaces.repositories.user import IUserRepository
from src.core.user.interfaces.senders.user import BaseUserHttpSender


class UserService:
    def __init__(
            self,
            repository: IUserRepository,
            publisher: IUserPublisher,
            http_sender: BaseUserHttpSender,
    ):
        self._repository = repository
        self._publisher = publisher
        self._sender = http_sender

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

    async def create_user(self, user_login: UserLoginDTO, user_info: UserInfoDTO) -> None:
        await self._validate_login(user_login.login)
        user_login.password = self._hash_password(user_login.password)
        user_id = await self._repository.save_into_db(user_login)
        user_info_to_broker = UserInfoToBrokerDTO(
            firstname=user_info.firstname,
            lastname=user_info.lastname,
            id=user_id
        )
        create_basket = CreateBasketDTO(user_id)
        await self._publisher.publish_create_basket(create_basket)
        await self._publisher.publish_create_user_info(user_info_to_broker)

    async def validate_user(self, user_login: UserLoginDTO) -> UserDTO:
        founded_user = await self._repository.get_user_by_login(user_login.login)
        if founded_user is None:
            raise LoginAuthException
        if not self._validate_password(user_login.password, founded_user.password):
            raise PasswordAuthException
        return founded_user

    async def get_user_info(self, authorization_cookies: CookieDTO) -> UserInfoDTO:
        return await self._sender.get_user_info(authorization_cookies)

    async def update_user_info(self, updated_user_info: UpdateUserInfoDTO) -> None:
        await self._publisher.publish_update_user_info(updated_user_info)

    async def update_user_login(self, updated_user_login: UpdateUserLoginDTO) -> None:
        if updated_user_login.login is not None:
            await self._validate_login(updated_user_login.login)
        if updated_user_login.password is not None:
            updated_user_login.password = self._hash_password(updated_user_login.password)
        await self._repository.update_user(updated_user_login)
