from datetime import datetime

from pydantic import BaseModel

from src.models.models import Organizations


class SOrganizationsModel(BaseModel):
    business_name: str
    delete_utc: datetime | None = None
    user_id: int


class SOrganizationsFilters(BaseModel):
    id: int | None = None
    business_name: str | None = None
    user_id: int | None = None


class SOrganizationResponse(BaseModel):
    business_name: str
    create_utc: datetime
    delete_utc: datetime | None
    user_id: int

    @staticmethod
    def from_orm(organization: Organizations) -> "SOrganizationResponse":
        return SOrganizationResponse(
            business_name=organization.business_name,
            create_utc=organization.create_utc,
            delete_utc=organization.delete_utc,
            user_id=organization.user_id,
        )

    @staticmethod
    def to_dict(organization: Organizations) -> dict:
        return {
            "business_name": organization.business_name,
            "create_utc": organization.create_utc,
            "delete_utc": organization.delete_utc,
            "user_id": organization.user_id,
        }


class SOrganizationAdd(BaseModel):
    business_name: str


class SOrganizationAddResponse(BaseModel):
    organization_id: int


class SOrganizationDeleteResponse(BaseModel):
    organization_id: int
