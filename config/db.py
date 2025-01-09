from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .config import POSTGRES_DB, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_HOST, POSTGRES_USER

db_url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
db_engine = create_async_engine(db_url, echo=False)
async_session_maker = async_sessionmaker(db_engine, expire_on_commit=False)


async def async_session():
    async with async_session_maker() as session:
        yield session