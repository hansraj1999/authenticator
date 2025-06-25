from db import db_manager
from datetime import datetime
import uuid
from sqlalchemy import text
from models import User as UserModel
from sqlalchemy import select


class User:
    def __init__(self):
        pass

    @staticmethod
    async def create_user(
        name: str,
        email: str,
        password_hash: str,
        is_email_verified: bool = False,
        service_name: str = "shorturl",
        last_generated_otp: str = None,
    ):
        async for session in db_manager.get_session():
            new_user = UserModel(
                id=uuid.uuid4(),
                name=name,
                email=email,
                password_hash=password_hash,
                is_email_verified=is_email_verified,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                service_name=service_name,
                last_generated_otp=last_generated_otp,
                last_generated_otp_sent_at=datetime.utcnow(),
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            return new_user

    @staticmethod
    async def get_all_users_paginated(page: int, page_size: int):
        async for session in db_manager.get_session():
            result = await session.execute(
                text(
                    f"SELECT * FROM users ORDER BY created_at DESC LIMIT {page_size} OFFSET {(page - 1) * page_size}"
                )
            )
            users = result.fetchall()
            return users

    @staticmethod
    async def get_user_by_id(user_id: str):
        async for session in db_manager.get_session():
            user = await session.get(User, user_id)
            return user

        return None

    @staticmethod
    async def get_user_by_email(email: str):
        async for session in db_manager.get_session():
            result = await session.execute(
                select(UserModel).where(UserModel.email == email)
            )
            user = result.scalar_one_or_none()
            return user

        return None
