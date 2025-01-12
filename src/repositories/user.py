from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..dto.user import UserLoginDTO, AbstractUserDTO, UserDTO
from ..models.user import UserModel


class UserRepository:
    model = UserModel

    def __init__(self, session: AsyncSession):
        self._session = session

    def _dto_to_model(self, user_dto: AbstractUserDTO) -> UserModel:
        user_login_data = user_dto.__dict__
        return self.model(**user_login_data)

    async def _get_user_model(self, **kwargs) -> UserModel | None:
        query = (
            select(self.model)
            .options(joinedload(UserModel.role))
            .filter_by(**kwargs)
        )
        return await self._session.scalar(query)

    async def save_into_db(self, user_login: UserLoginDTO) -> None:
        user_login_model = self._dto_to_model(user_login)
        self._session.add(user_login_model)
        await self._session.commit()

    async def get_user_by_login(self, login: str) -> UserDTO | None:
        user_model = await self._get_user_model(login=login)
        if user_model is not None:
            return UserDTO(
                id=user_model.user_id,
                login=user_model.login,
                password=user_model.password,
                role=user_model.role.role_name,
            )
