import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.user.dto.user import UserLoginDTO, AbstractUserDTO, UserDTO, UpdateUserLoginDTO
from src.core.user.interfaces.repositories.user import IUserRepository
from src.core.user.models.user import UserModel


class UserRepository(IUserRepository):
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

    async def save_into_db(self, user_login: UserLoginDTO) -> uuid.UUID:
        user_login_model = self._dto_to_model(user_login)
        self._session.add(user_login_model)
        await self._session.commit()
        return user_login_model.user_id

    async def get_user_by_login(self, login: str) -> UserDTO | None:
        user_model = await self._get_user_model(login=login)
        if user_model is not None:
            return UserDTO(
                id=user_model.user_id,
                login=user_model.login,
                password=user_model.password,
                role=user_model.role.role_name,
            )

    async def update_user(self, updated_user_login: UpdateUserLoginDTO):
        user_model = await self._get_user_model(user_id=updated_user_login.id)
        for key, value in updated_user_login.__dict__.items():
            if key == "id" or value is None:
                continue
            setattr(user_model, key, value)
        await self._session.commit()
