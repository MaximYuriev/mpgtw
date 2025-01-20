from aiohttp import ClientSession

from config import USER_SERVICE_GET_USER_INFO_URL
from ..dto.cookie import CookieDTO
from ..dto.user import UserInfoDTO
from ..dto.http import HttpResponseDTO
from ..exceptions.http.sender import HttpSenderRequestException, HttpSenderValidateException


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
                USER_SERVICE_GET_USER_INFO_URL,
                cookies=((cookie.key, cookie.value),)
            )
            response_body = await response.json()
            user_service_response = cls._validate_responses(response_body)
            if response.status == 200:
                return UserInfoDTO(**user_service_response.data)
            raise HttpSenderRequestException(response.status, user_service_response.detail)