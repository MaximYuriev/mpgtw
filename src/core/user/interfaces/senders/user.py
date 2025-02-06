from abc import ABC, abstractmethod

from src.core.commons.dto.cookie import CookieDTO
from src.core.commons.sender import BaseHttpSender
from src.core.user.dto.user import UserInfoDTO


class BaseUserHttpSender(ABC, BaseHttpSender):
    _USER_SERVICE_URL = "http://localhost:8004"
    _GET_USER_INFO_URL = f"{_USER_SERVICE_URL}/user"

    @abstractmethod
    async def get_user_info(self, cookie: CookieDTO) -> UserInfoDTO:
        ...
