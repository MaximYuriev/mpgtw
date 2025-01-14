import uuid

from auth.payloads import AccessPayload, RefreshPayload, BasePayload
from auth.token import JWT
from ..dto.token import RefreshTokenDTO
from ..exceptions.token import TokenNotFoundException
from ..dto.user import UserDTO
from ..repositories.token import TokenRepository


class AuthService:
    def __init__(self, repository: TokenRepository):
        self._repository = repository

    @staticmethod
    def _create_access_payload(user: UserDTO) -> AccessPayload:
        return AccessPayload(
            sub=str(user.id),
            role=user.role,
        )

    @staticmethod
    def _create_refresh_payload(user: UserDTO) -> RefreshPayload:
        return RefreshPayload(sub=str(user.id))

    @staticmethod
    def _create_token(token_payload: BasePayload) -> str:
        return JWT.create_jwt(token_payload)

    @staticmethod
    def _parse_token(token: str) -> dict:
        return JWT.parse_jwt(token)

    def _create_access_token(self, user: UserDTO) -> str:
        access_token_payload = self._create_access_payload(user)
        return self._create_token(access_token_payload)

    async def _create_refresh_token(self, user: UserDTO) -> None:
        refresh_token_payload = self._create_refresh_payload(user)
        refresh_token = self._create_token(refresh_token_payload)
        refresh_token_dto = RefreshTokenDTO(refresh_token, refresh_token_payload.sub)
        await self._repository.save_token(refresh_token_dto)

    async def _get_refresh_token(self, user_id: uuid.UUID | str) -> RefreshTokenDTO:
        return await self._repository.get_token(user_id)

    async def auth_user(self, user: UserDTO) -> str:
        access_token = self._create_access_token(user)
        try:
            await self._get_refresh_token(user.id)
        except TokenNotFoundException:
            await self._create_refresh_token(user)
        finally:
            return access_token
