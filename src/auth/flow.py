import logging
import random
import secrets
import string

import aiohttp
from authlib.integrations.starlette_client import OAuthError
from fastapi import HTTPException, Request, Response, status
from pydantic import EmailStr
from sqlalchemy.exc import SQLAlchemyError

from src.auth.auth import (authenticate_user, create_access_token,
                           get_hash_password)
from src.config import settings
from src.logger import config_logger
from src.models.enums import UsersRoleEnum
from src.users.schema import (SUsersAuth, SUsersAuthResponse, SUsersModel,
                              SUsersRegistration, SUsersRegistrationResponse)
from src.utils.decorator import async_retry
from src.utils.dependency import UsersServiceDep
from src.utils.exception import (CredentialsException, InvalidAdminToken,
                                 InvalidEmailException)

logger = logging.getLogger(__name__)

# Configure logger
config_logger()


class AuthFlow:
    def __init__(self, users_service: UsersServiceDep | None = None):
        self.users_service = users_service

    async def register_flow(
        self, data: SUsersRegistration
    ) -> SUsersRegistrationResponse:
        # Get password hash
        hashed_password = get_hash_password(data.password)

        # Check email
        valid_email = await self.validate_email(data.email)
        if not valid_email:
            raise InvalidEmailException

        # Check for ADMIN_TOKEN
        if data.admin_token and data.role == UsersRoleEnum.Admin:
            if not secrets.compare_digest(
                data.admin_token.encode(), settings.ADMIN_TOKEN.encode()
            ):
                raise InvalidAdminToken

        try:
            user_id = await self.users_service.add(
                SUsersModel.from_orm(data, hashed_password)
            )
            return SUsersRegistrationResponse(user_id=user_id, registered=True)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("[Db error]: %s" % ex)
            else:
                logger.error("[Unknown error]: %s" % ex)
            return SUsersRegistrationResponse(user_id=None, registered=False)

    async def authenticate_flow(
        self, response: Response, data: SUsersAuth
    ) -> SUsersAuthResponse:
        try:
            user = await authenticate_user(
                data.email, data.password, self.users_service
            )
            access_token = create_access_token({"sub": str(user.id)})
            response.set_cookie(
                "access_token",
                access_token,
                httponly=True,
                max_age=settings.TOKEN_EXPIRE,
            )
            response.headers["Authorization"] = access_token
            return SUsersAuthResponse(access_token=access_token)
        except Exception as ex:
            if isinstance(ex, SQLAlchemyError):
                logger.error("Db error: %s" % ex)
            else:
                logger.error("Unknown error: %s" % ex)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    async def google_oauth_flow(self, request: Request):
        from src.auth.view import oauth

        url = request.url_for("google_oauth_callback")
        return await oauth.google.authorize_redirect(request, url)

    async def google_oauth_callback_flow(
        self, request: Request, response: Response
    ) -> SUsersAuthResponse:
        from src.auth.view import oauth

        try:
            token = await oauth.google.authorize_access_token(request)
        except OAuthError as ex:
            logger.error("OAuthError: %s" % ex)
            raise CredentialsException

        # Get or Create User
        user_info = token.get("userinfo")
        user = await self.users_service.get_or_create(
            SUsersModel(
                username=user_info.get("name"),
                email=user_info.get("email"),
                phone=None,
                role=UsersRoleEnum.Owner,
                hashed_password=get_hash_password(
                    "".join(random.sample(string.ascii_letters + string.digits, 8))
                ),
            )
        )

        # Create access_token
        sub = str(user) if isinstance(user, int) else str(user.id)
        access_token = create_access_token({"sub": sub})
        response.set_cookie(
            "access_token", access_token, httponly=True, max_age=settings.TOKEN_EXPIRE
        )
        response.headers["Authorization"] = access_token
        return SUsersAuthResponse(access_token=access_token)

    @staticmethod
    @async_retry(5)
    async def validate_email(email: EmailStr):
        headers = {
            "x-rapidapi-host": settings.X_RAPIDAPI_HOST,
            "x-rapidapi-key": settings.X_RAPIDAPI_KEY,
        }
        params = {"email": email}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://email-checker.p.rapidapi.com/verify/v1",
                headers=headers,
                params=params,
            ) as response:
                result = await response.json()
                return True if result["status"] == "valid" else False
