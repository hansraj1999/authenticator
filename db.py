from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
import os
from sqlalchemy.orm import sessionmaker
import redis

DATABASE_URL = os.environ.get("MYSQL_CONNECTION_STRING")
REDIS_HOST = os.getenv("REDIS_HOST", "default")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_USERNAME = os.getenv("REDIS_USERNAME", "default")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "default")


class DB:
    _engine = None
    _sessionmaker = None
    _redis_connection = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            cls._engine = create_async_engine(DATABASE_URL, echo=True, future=True)
        return cls._engine

    @classmethod
    def get_sessionmaker(cls):
        if cls._sessionmaker is None:
            cls._sessionmaker = async_sessionmaker(
                cls.get_engine(), expire_on_commit=False, class_=AsyncSession
            )
        return cls._sessionmaker

    @classmethod
    async def get_session(cls) -> AsyncSession:
        async_session = cls.get_sessionmaker()
        async with async_session() as session:
            yield session

    @classmethod
    def get_redis_connection(cls):
        if cls._redis_connection is not None:
            return cls._redis_connection
        cls._redis_connection = redis.StrictRedis(
            host=REDIS_HOST,
            port=int(REDIS_PORT),
            decode_responses=True,
            username=REDIS_USERNAME,
            password=REDIS_PASSWORD,
        )
        return cls._redis_connection


# Declarative base (can import from here)
Base = declarative_base()
db_manager = DB()
