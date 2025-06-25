from pydantic import BaseModel, Field

from src.models.models import OrganizationRates


class SOrganizationRatesModel(BaseModel):
    stars: int = Field(le=5, ge=1)
    notes: str | None = None
    user_id: int
    organization_id: int


class SOrganizationRatesFilters(BaseModel):
    stars: int | None = None
    user_id: int | None = None
    organization_id: int | None = None


class SOrganizationRate(BaseModel):
    stars: int
    notes: str | None
    user_id: int

    @staticmethod
    def to_dict(organization_rate: OrganizationRates) -> dict:
        return {
            "stars": organization_rate.stars,
            "notes": organization_rate.notes,
            "user_id": organization_rate.user_id,
        }


class SOrganizationRatesResponse(BaseModel):
    TotalCount: int
    Data: list[SOrganizationRate]


class SOrganizationRateAdd(BaseModel):
    stars: int = Field(ge=1, le=5)
    notes: str | None = None


class SOrganizationRateAddResponse(BaseModel):
    rate_id: int
