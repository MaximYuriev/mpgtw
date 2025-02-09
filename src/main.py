from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.api.product.router import product_router
from src.api.user.routers.auth import auth_router
from src.api.user.routers.user import user_router
from src.config import Config
from src.ioc import UserProvider, AuthProvider, SQLAlchemyProvider, RMQProvider, AiohttpProvider, ProductProvider

config = Config()
container = make_async_container(
    UserProvider(),
    AuthProvider(),
    ProductProvider(),
    SQLAlchemyProvider(),
    RMQProvider(),
    AiohttpProvider(),
    context={Config: config},
)
app = FastAPI(title="API Gateway")

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(product_router)

setup_dishka(container, app)
