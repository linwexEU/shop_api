from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status

from src.config import settings
from src.db.db import AsyncSessionDep
from src.models.enums import UsersRoleEnum
from src.models.models import Users
from src.users.schema import SUserAuthModel, SUsersFilters
from src.utils.dependency import UsersServiceDep
from src.utils.exception import AccessAdminException, AccessOwnerException


async def get_token(request: Request):
    token = (
        request.cookies.get("access_token")
        if request.cookies.get("access_token")
        else request.headers.get("Authorization")
    )
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(
    token: Annotated[str, Depends(get_token)], users_service: UsersServiceDep, session: AsyncSessionDep
) -> SUserAuthModel:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire = payload.get("exp")
    if not expire or int(expire) < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = await users_service.get_by_filters(SUsersFilters(id=int(user_id)), session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return SUserAuthModel.from_orm(user)


CurrentUserDep = Annotated[Users, Depends(get_current_user)]


async def get_admin_user(current_user: CurrentUserDep) -> SUserAuthModel:
    if current_user.role != UsersRoleEnum.Admin:
        raise AccessAdminException
    return SUserAuthModel.from_orm(current_user)


async def get_owner_user(current_user: CurrentUserDep) -> SUserAuthModel:
    if current_user.role != UsersRoleEnum.Owner:
        raise AccessOwnerException
    return SUserAuthModel.from_orm(current_user)


AdminUserDep = Annotated[Users, Depends(get_admin_user)]
OwnerUserDep = Annotated[Users, Depends(get_owner_user)]
