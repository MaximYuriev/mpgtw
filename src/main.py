from fastapi import FastAPI

from src.routers.user import user_router
from src.routers.auth import auth_router

app = FastAPI(title="API Gateway")

app.include_router(user_router)
app.include_router(auth_router)