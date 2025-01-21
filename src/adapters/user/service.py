import uuid

from src.dto.cookie import CookieDTO
from src.dto.user import UserLoginDTO, UserDTO, UserInfoDTO, UpdateUserInfoDTO
from src.schemas.user import CreateUserSchema, UserLoginSchema, UserInfoSchema
from src.services.user import UserService


class UserAdapter:
    def __init__(self, user_service: UserService):
        self._service = user_service

    async def create_user(
            self,
            create_user_schema: CreateUserSchema,
    ) -> None:
        user_login = UserLoginDTO(
            login=create_user_schema.login,
            password=create_user_schema.password,
        )
        user_info = UserInfoDTO(
            firstname=create_user_schema.firstname,
            lastname=create_user_schema.lastname,
        )
        await self._service.create_user(user_login, user_info)

    async def validate_user(
            self,
            user_login_schema: UserLoginSchema,
    ) -> UserDTO:
        user_login = UserLoginDTO(
            login=user_login_schema.login,
            password=user_login_schema.password,
        )
        return await self._service.validate_user(user_login)

    async def get_user_info(
            self,
            cookies: CookieDTO,
    ) -> UserInfoSchema:
        user_info = await self._service.get_user_info(cookies)
        return UserInfoSchema(**user_info.__dict__)

    async def update_user_info(
            self,
            user_id: uuid.UUID,
            user_info_schema: UserInfoSchema,
    ) -> None:
        update_user_info_data = user_info_schema.model_dump()
        update_user_info = UpdateUserInfoDTO(
            id=user_id,
            **update_user_info_data
        )
        await self._service.update_user_info(update_user_info)
