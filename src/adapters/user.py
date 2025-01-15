from ..dto.user import UserLoginDTO, UserDTO, UserInfoDTO
from ..schemas.user import CreateUserSchema, UserLoginSchema
from ..services.user import UserService


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
