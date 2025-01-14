from auth.payloads import AccessPayload, RefreshPayload, BasePayload
from auth.token import JWT
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
    def _create_token(token_payload: BasePayload) -> str:
        return JWT.create_jwt(token_payload)

    async def auth_user(self, user: UserDTO) -> str:
        access_token_payload = self._create_access_payload(user)
        access_token = self._create_token(access_token_payload)
        try:
            await self._get_refresh_token(user.id)
        except TokenNotFoundException:
            ...
        finally:
            return access_token
