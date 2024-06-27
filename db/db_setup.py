# stdlib
from typing import AsyncGenerator

# thirdparty
import redis
from redis import asyncio as aioredis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

# project
import settings
from settings import DATABASE_URL, DATABASE_URL_PSYCOPG2

engine = create_engine(DATABASE_URL_PSYCOPG2)

Base = declarative_base()

Session = sessionmaker(bind=engine)
ScopedSession = scoped_session(Session)

async_engine = create_async_engine(
    DATABASE_URL, pool_size=settings.ASYNC_ENGINE_POOL_SIZE, max_overflow=settings.ASYNC_ENGINE_MAX_OVERFLOW
)
async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)  # noqa


def create_redis():
    return aioredis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


def create_redis_sync():
    return redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


redis_connection_pool = create_redis()
redis_connection_pool_sync = create_redis_sync()
