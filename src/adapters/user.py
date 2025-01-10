from ..domains.user import UserLogin
from ..schemas.user import CreateUserSchema
from ..services.user import UserService


class UserAdapter:
    def __init__(self, user_service: UserService):
        self._service = user_service

    async def create_user(
            self,
            create_user_schema: CreateUserSchema,
    ) -> None:
        user_login = UserLogin(
            login=create_user_schema.login,
            password=create_user_schema.password,
        )
        await self._service.create_user(user_login)
