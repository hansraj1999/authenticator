from datetime import datetime
import uuid

from sqlalchemy import Boolean, Column, String, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, default=lambda: uuid.uuid4().bytes)
    name = Column(String(255))
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_email_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    service_name = Column(String(255), nullable=False, default="shorturl")
    last_generated_otp = Column(String(255), nullable=True)
    last_generated_otp_sent_at = Column(TIMESTAMP, nullable=True)

    sessions = relationship(
        "Session", back_populates="user", cascade="all, delete-orphan"
    )
    reset_tokens = relationship(
        "PasswordResetToken", back_populates="user", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("service_name", "email", name="uq_user_service_name_email"),
    )


class Session(Base):
    __tablename__ = "sessions"
    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(255), default=lambda: str(uuid.uuid4()))
    user_id = Column(
        String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    expires_at = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sessions")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String(255), primary_key=True, default=lambda: uuid.uuid4().bytes)
    user_id = Column(
        String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token = Column(String(255), unique=True)
    expires_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="reset_tokens")
