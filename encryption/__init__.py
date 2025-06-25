import bcrypt

import logging

logger = logging.getLogger(__name__)

from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_encrypted_password(password) -> str:
    password = pwd_cxt.hash(password)
    return password


def validate_password(password: str, stored_hash: str) -> bool:
    return pwd_cxt.hash(password) == stored_hash
