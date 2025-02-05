from aiohttp import ClientSession

from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.dto.http_response import HttpResponseDTO
from src.core.commons.exceptions.sender import HttpSenderRequestException, HttpSenderValidateException
from src.core.user.dto.user import UserInfoDTO


class UserServiceHttpSender:
    @staticmethod
    def _validate_responses(response_body: dict) -> HttpResponseDTO:
        try:
            return HttpResponseDTO(**response_body)
        except TypeError:
            raise HttpSenderValidateException

    @classmethod
    async def get_user_info(cls, cookie: CookieDTO) -> UserInfoDTO:
        async with ClientSession() as session:
            response = await session.get(
                "",
                cookies=((cookie.key, cookie.value),)
            )
            response_body = await response.json()
            user_service_response = cls._validate_responses(response_body)
            if response.status == 200:
                return UserInfoDTO(**user_service_response.data)
            raise HttpSenderRequestException(response.status, user_service_response.detail)