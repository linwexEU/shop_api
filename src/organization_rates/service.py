from src.db.db import AsyncSessionDep
from src.models.models import OrganizationRates
from src.organization_rates.repository import PersistenceOrganizationRatesRepository
from src.organization_rates.schema import SOrganizationRatesFilters, SOrganizationRatesModel
from src.utils.uow import UnitOfWork


class OgranizationRatesService:
    def __init__(self, org_rates_repo: PersistenceOrganizationRatesRepository):
        self.org_rates_repo: PersistenceOrganizationRatesRepository = org_rates_repo()

    async def add(self, data: SOrganizationRatesModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.org_rates_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SOrganizationRatesFilters, session: AsyncSessionDep, one: bool = True) -> list[OrganizationRates] | OrganizationRates:
        return await self.org_rates_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)
