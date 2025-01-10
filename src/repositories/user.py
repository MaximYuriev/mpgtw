import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..domains.user import UserLogin
from ..models.user import UserModel


class UserRepository:
    domain = UserLogin
    model = UserModel

    def __init__(self, session: AsyncSession):
        self._session = session

    def _domain_to_model(self, user_login: domain) -> model:
        return self.model(
            login=user_login.login,
            password=user_login.password,
        )

    def _model_to_domain(self, user_login_model: model) -> domain:
        return self.domain(
            login=user_login_model.login,
            password=user_login_model.password,
        )

    async def _get_user_login_model(self, **kwargs) -> model | None:
        query = select(self.model).filter_by(**kwargs)
        return await self._session.scalar(query)

    async def save_into_db(self, user_login: domain) -> uuid.UUID:
        user_login_model = self._domain_to_model(user_login)
        self._session.add(user_login_model)
        await self._session.commit()
        return user_login_model.user_id

    async def get_user_login(self, login: str) -> domain | None:
        user_login_model = await self._get_user_login_model(login=login)
        if user_login_model is not None:
            return self._model_to_domain(user_login_model)
