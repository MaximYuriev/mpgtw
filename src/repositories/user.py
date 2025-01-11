from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..dto.user import UserLoginDTO, UserPayloadDTO, UserDTO
from ..models.user import UserModel, RoleModel


class UserRepository:
    model = UserModel

    def __init__(self, session: AsyncSession):
        self._session = session

    def _dto_to_model(self, user_dto: UserDTO) -> UserModel:
        user_login_data = user_dto.__dict__
        return self.model(**user_login_data)

    async def _get_user_model(self, **kwargs) -> UserModel | None:
        query = select(self.model).filter_by(**kwargs)
        return await self._session.scalar(query)

    async def save_into_db(self, user_login: UserLoginDTO) -> None:
        user_login_model = self._dto_to_model(user_login)
        self._session.add(user_login_model)
        await self._session.commit()

    async def get_user_login(self, login: str) -> UserLoginDTO | None:
        user_login_model = await self._get_user_model(login=login)
        if user_login_model is not None:
            return UserLoginDTO(
                login=user_login_model.login,
                password=user_login_model.password,
            )

    async def get_user_payload(self, login: str) -> UserPayloadDTO | None:
        query = (
            select(
                UserModel.user_id,
                RoleModel.role_name
            ).join(
                RoleModel,
                UserModel.role_id == RoleModel.role_id
            ).where(
                UserModel.login == login
            )
        )
        result_orm = await self._session.execute(query)
        result = result_orm.first()
        if result is not None:
            return UserPayloadDTO(
                sub=result[0],
                role=result[1]
            )
