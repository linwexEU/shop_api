from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr

from src.config import settings
from src.db.db import AsyncSessionDep
from src.users.schema import SUsersFilters
from src.utils.dependency import UsersServiceDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def authenticate_user(
    email: EmailStr, password: str, users_service: UsersServiceDep, session: AsyncSessionDep
):
    user = await users_service.get_by_filters(SUsersFilters(email=email), session)
    if not (user and verify_password(password, user.hashed_password)):
        return False
    return user
