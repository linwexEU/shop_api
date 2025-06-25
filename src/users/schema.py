from pydantic import BaseModel, EmailStr

from src.models.enums import UsersRoleEnum
from src.models.models import Users


class SUsersFilters(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    role: UsersRoleEnum | None = None


class SUsersRegistration(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str | None = None
    role: UsersRoleEnum
    admin_token: str | None = None


class SUsersRegistrationResponse(BaseModel):
    user_id: int | None = None
    registered: bool


class SUsersModel(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    phone: str | None = None
    role: UsersRoleEnum

    @staticmethod
    def from_orm(data: SUsersRegistration, hashed_password: str) -> "SUsersModel":
        return SUsersModel(
            username=data.username,
            email=data.email,
            hashed_password=hashed_password,
            phone=data.phone if data.phone else None,
            role=data.role,
        )


class SUsersAuth(BaseModel):
    email: EmailStr
    password: str


class SUsersAuthResponse(BaseModel):
    access_token: str


class SUserAuthModel(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str | None = None
    role: UsersRoleEnum

    @staticmethod
    def from_orm(user: Users) -> "SUserAuthModel":
        return SUserAuthModel(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
            role=user.role,
        )
