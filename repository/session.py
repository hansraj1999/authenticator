from db import db_manager
from models import Session as SessionModel
from datetime import datetime
import uuid
import logging
from sqlalchemy import text
from models import User as UserModel
from sqlalchemy import select
from typing import Optional

logger = logging.getLogger(__name__)


class Session:
    @staticmethod
    async def get_session_by_user_id(user_id: str, is_active: bool = True):
        async for session in db_manager.get_session():
            query = select(SessionModel).where(
                SessionModel.user_id == user_id, SessionModel.is_active == is_active
            )
            result = await session.execute(query)
            _session = result.scalar_one_or_none()
            return _session

        return None

    @staticmethod
    async def get_session_by_token(token: str, is_active: bool = True):
        async for session in db_manager.get_session():
            query = select(SessionModel).where(
                SessionModel.session_id == token, SessionModel.is_active == is_active
            )
            result = await session.execute(query)
            _session = result.scalar_one_or_none()
            return _session

        return None

    @staticmethod
    def check_if_session_is_expired(expires_at: datetime):
        if expires_at is None:
            return False
        return expires_at < datetime.utcnow()

    @staticmethod
    async def upsert_session(user_id: str, expires_at: datetime = None):
        # put token in redis cache
        async for session in db_manager.get_session():
            _session = await Session.get_session_by_user_id(user_id)
            if _session is None:
                _session = SessionModel(user_id=user_id, expires_at=expires_at)
                session.add(_session)
            else:
                _session.expires_at = expires_at
            await session.commit()
            ttl = None
            if _session.expires_at:
                ttl = (_session.expires_at - datetime.utcnow()).seconds
            Session.add_token_in_cache(
                "token",
                str({"user_id": _session.user_id, "token": _session.session_id}),
                ttl=ttl,
            )  # TODO: change ttl
            return _session

    @staticmethod
    def add_token_in_cache(key, value, ttl=None):  # TODO: change ttl
        db_manager.get_redis_connection().set(key, value)
        if ttl:
            db_manager.get_redis_connection().expire(key, ttl)
        logger.info(f"Added Token in cache: {key}")

    @staticmethod
    def get_token_from_cache(key):
        token = db_manager.get_redis_connection.get(key)
        return token

    @staticmethod
    async def get_sessions_paginated(
        page: int, page_size: int, is_active: Optional[bool] = None
    ):
        query = "SELECT * FROM sessions"
        if is_active is not None:
            query += f" WHERE is_active = {is_active}"
        query += f" ORDER BY created_at DESC LIMIT {page_size} OFFSET {(page - 1) * page_size}"

        async for session in db_manager.get_session():
            result = await session.execute(text(query))
            _sessions = result.fetchall()
            return _sessions
        return []
