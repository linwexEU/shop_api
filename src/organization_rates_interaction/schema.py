from pydantic import BaseModel


class SOrganizationRatesInteractionModel(BaseModel):
    user_id: int
    organization_id: int


class SOrganizationRatesInteractionFilters(BaseModel):
    user_id: int | None = None
    organization_id: int | None = None
