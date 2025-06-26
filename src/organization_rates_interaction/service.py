from src.models.models import OrganizationRatesInteraction
from src.db.db import AsyncSessionDep
from src.organization_rates_interaction.repository import PersistenceOrganizationRatesInteractionRepository
from src.organization_rates_interaction.schema import SOrganizationRatesInteractionFilters, SOrganizationRatesInteractionModel
from src.utils.uow import UnitOfWork


class OrganizationRatesInteractrionService:
    def __init__(self, org_rates_inter_repo: PersistenceOrganizationRatesInteractionRepository):
        self.org_rates_inter_repo: PersistenceOrganizationRatesInteractionRepository = org_rates_inter_repo()

    async def add(self, data: SOrganizationRatesInteractionModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.org_rates_inter_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SOrganizationRatesInteractionFilters, session: AsyncSessionDep, one: bool = True) -> list[OrganizationRatesInteraction] | OrganizationRatesInteraction:
        return await self.org_rates_inter_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)
