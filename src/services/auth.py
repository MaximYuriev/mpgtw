import uuid

from auth.payloads import AccessPayload, RefreshPayload, BasePayload
from auth.token import JWT
from auth.exceptions import AuthTokenInvalidException, AuthTokenExpiredException
from ..dto.token import RefreshTokenDTO
from ..exceptions.application.token import TokenNotFoundException, TokenExpiredException, TokenInvalidException
from ..dto.user import UserDTO
from ..repositories.token import TokenRepository


class AuthService:
    def __init__(self, repository: TokenRepository):
        self._repository = repository

    @staticmethod
    def _create_access_payload(sub: str, role: str) -> AccessPayload:
        return AccessPayload(
            sub=sub,
            role=role,
        )

    @staticmethod
    def _create_refresh_payload(user: UserDTO) -> RefreshPayload:
        return RefreshPayload(sub=str(user.id))

    @staticmethod
    def _create_token(token_payload: BasePayload) -> str:
        return JWT.create_jwt(token_payload)

    @staticmethod
    def _parse_token(token: str, verify_expire: bool = True) -> dict:
        return JWT.parse_jwt(token, verify_expire)

    def _create_access_token(self, access_token_payload: AccessPayload) -> str:
        return self._create_token(access_token_payload)

    async def _create_refresh_token(self, refresh_token_payload: RefreshPayload) -> None:
        refresh_token = self._create_token(refresh_token_payload)
        refresh_token_dto = RefreshTokenDTO(refresh_token, refresh_token_payload.sub)
        await self._repository.save_token(refresh_token_dto)

    async def _get_refresh_token(self, user_id: uuid.UUID | str) -> RefreshTokenDTO:
        return await self._repository.get_token(user_id)

    def _validate_token(self, token: str) -> None:
        try:
            self._parse_token(token)
        except AuthTokenExpiredException:
            raise TokenExpiredException
        except AuthTokenInvalidException:
            raise TokenInvalidException

    def _parse_access_token(self, access_token: str, verify_expire: bool = True) -> AccessPayload:
        access_token_payload_data = self._parse_token(access_token, verify_expire)
        return AccessPayload(**access_token_payload_data)

    async def auth_user(self, user: UserDTO) -> str:
        access_token_payload = self._create_access_payload(
            sub=str(user.id),
            role=user.role,
        )
        access_token = self._create_access_token(access_token_payload)
        try:
            refresh_token = await self._get_refresh_token(user.id)
        except TokenNotFoundException:
            refresh_token_payload = self._create_refresh_payload(user)
            await self._create_refresh_token(refresh_token_payload)
        else:
            try:
                self._validate_token(refresh_token.refresh_token)
            except TokenInvalidException:
                await self._repository.delete_token(refresh_token)
                refresh_token_payload = self._create_refresh_payload(user)
                await self._create_refresh_token(refresh_token_payload)
        finally:
            return access_token

    async def refresh_access_token(self, access_token: str) -> str:
        access_token_payload = self._parse_access_token(access_token, verify_expire=False)
        refresh_token = await self._get_refresh_token(access_token_payload.sub)
        self._validate_token(refresh_token.refresh_token)
        new_access_token_payload = self._create_access_payload(
            sub=access_token_payload.sub,
            role=access_token_payload.role
        )
        return self._create_access_token(new_access_token_payload)
