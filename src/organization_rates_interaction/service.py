from src.organization_rates_interaction.repository import \
    OrganizationRatesInteractionRepository
from src.organization_rates_interaction.schema import (
    SOrganizationRatesInteractionFilters, SOrganizationRatesInteractionModel)


class OrganizationRatesInteractrionService:
    def __init__(self, org_rates_inter_repo: OrganizationRatesInteractionRepository):
        self.org_rates_inter_repo: OrganizationRatesInteractionRepository = (
            org_rates_inter_repo()
        )

    async def add(self, data: SOrganizationRatesInteractionModel) -> int:
        return await self.org_rates_inter_repo.add(data.model_dump())

    async def get_by_filters(
        self, filters: SOrganizationRatesInteractionFilters, one=True
    ):
        return await self.org_rates_inter_repo.get_by_filters(
            filters.model_dump(exclude_none=True), one
        )
