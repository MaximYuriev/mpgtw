from typing import AsyncIterable

from aiohttp import ClientSession
from dishka import Provider, from_context, Scope, provide
from faststream.rabbit import RabbitBroker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from src.api.basket.adapter import BasketServiceAdapter
from src.api.product.adapter import ProductServiceAdapter
from src.api.user.adapters.user import UserAdapter
from src.config import Config
from src.core.basket.interfaces.sender import BaseBasketHttpSender
from src.core.basket.sender import BasketHttpSender
from src.core.basket.service import BasketService
from src.core.product.interfaces.sender import BaseProductHttpSender
from src.core.product.sender import ProductHttpSender
from src.core.product.service import ProductService
from src.core.user.broker.publishers.user import UserPublisher
from src.core.user.interfaces.publishers.user import IUserPublisher
from src.core.user.interfaces.repositories.token import ITokenRepository
from src.core.user.interfaces.repositories.user import IUserRepository
from src.core.user.interfaces.senders.user import BaseUserHttpSender
from src.core.user.repositories.token import TokenRepository
from src.core.user.repositories.user import UserRepository
from src.core.user.senders.user import UserServiceHttpSender
from src.core.user.services.auth import AuthService
from src.core.user.services.user import UserService


class SQLAlchemyProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_async_engine(self, config: Config) -> AsyncEngine:
        return create_async_engine(config.postgres.db_url, echo=False)

    @provide(scope=Scope.APP)
    def get_async_session_maker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session


class RMQProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_broker_connection(self, config: Config) -> AsyncIterable[RabbitBroker]:
        async with RabbitBroker(config.rmq.rmq_url) as broker:
            yield broker


class AiohttpProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_http_connection(self) -> AsyncIterable[ClientSession]:
        async with ClientSession() as session:
            yield session


class UserProvider(Provider):
    scope = Scope.REQUEST

    user_repository = provide(UserRepository, provides=IUserRepository)
    user_publisher = provide(UserPublisher, provides=IUserPublisher)
    user_sender = provide(UserServiceHttpSender, provides=BaseUserHttpSender)
    user_service = provide(UserService)
    user_service_adapter = provide(UserAdapter)


class AuthProvider(Provider):
    scope = Scope.REQUEST

    auth_repository = provide(TokenRepository, provides=ITokenRepository)
    auth_service = provide(AuthService)


class ProductProvider(Provider):
    scope = Scope.REQUEST

    product_sender = provide(ProductHttpSender, provides=BaseProductHttpSender)
    product_service = provide(ProductService)
    product_adapter = provide(ProductServiceAdapter)


class BasketProvider(Provider):
    scope = Scope.REQUEST

    basket_sender = provide(BasketHttpSender, provides=BaseBasketHttpSender)
    basket_service = provide(BasketService)
    basket_adapter = provide(BasketServiceAdapter)
