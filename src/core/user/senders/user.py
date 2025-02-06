from aiohttp import ClientSession

from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.exceptions.sender import HttpSenderRequestException
from src.core.user.dto.user import UserInfoDTO
from src.core.user.interfaces.senders.user import BaseUserHttpSender


class UserServiceHttpSender(BaseUserHttpSender):
    def __init__(self, session: ClientSession):
        self._session = session

    async def get_user_info(self, cookie: CookieDTO) -> UserInfoDTO:
        response = await self._session.get(
            self._GET_USER_INFO_URL,
            cookies=((cookie.key, cookie.value),)
        )
        response_body = await response.json()
        user_service_response = self._validate_responses(response_body)
        if response.status == 200:
            return UserInfoDTO(**user_service_response.data)
        raise HttpSenderRequestException(response.status, user_service_response.detail)
