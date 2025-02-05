from abc import ABC, abstractmethod

from src.core.user.dto.basket import CreateBasketDTO
from src.core.user.dto.user import UserInfoToBrokerDTO, UpdateUserInfoDTO


class IUserPublisher(ABC):
    @abstractmethod
    async def publish_create_user_info(self, user_info: UserInfoToBrokerDTO) -> None:
        ...

    @abstractmethod
    async def publish_update_user_info(self, update_user_info: UpdateUserInfoDTO) -> None:
        ...

    @abstractmethod
    async def publish_create_basket(self, create_basket_schema: CreateBasketDTO) -> None:
        ...
