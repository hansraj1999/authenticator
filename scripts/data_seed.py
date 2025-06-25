from datetime import datetime
import uuid
import os

os.system("pip install pymysql")
from sqlalchemy import (
    create_engine,
    Boolean,
    Column,
    String,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Define base
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True, default=lambda: uuid.uuid4().hex)
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
    id = Column(String(255), primary_key=True, default=lambda: uuid.uuid4().hex)
    session_id = Column(String(255), default=lambda: uuid.uuid4().hex)
    user_id = Column(
        String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    expires_at = Column(TIMESTAMP)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="sessions")


class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(String(255), primary_key=True, default=lambda: uuid.uuid4().hex)
    user_id = Column(
        String(255), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    token = Column(String(255), unique=True)
    expires_at = Column(TIMESTAMP)

    user = relationship("User", back_populates="reset_tokens")


DATABASE_URL = os.getenv("MYSQL_CONNECTION_STRING")
prefix, rest = DATABASE_URL.split("://", 1)

new_prefix = "mysql+pymysql"
DATABASE_URL = f"{new_prefix}://{rest}"

engine = create_engine(DATABASE_URL)


def main():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)
    print("Tables created successfully.")
