from datetime import datetime

from src.models.models import Organizations
from src.db.db import AsyncSessionDep
from src.organizations.repository import PersistenceOrganizationsRepository
from src.organizations.schema import SOrganizationsFilters, SOrganizationsModel
from src.utils.uow import UnitOfWork


class OrganizationsService:
    def __init__(self, org_repo: PersistenceOrganizationsRepository):
        self.org_repo: PersistenceOrganizationsRepository = org_repo()

    async def add(self, data: SOrganizationsModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.org_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SOrganizationsFilters, session: AsyncSessionDep, one: bool = True) -> list[Organizations] | Organizations:
        return await self.org_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)

    async def add_delete_utc(self, organization_id: int, delete_utc: datetime, session: AsyncSessionDep) -> None:
        async with UnitOfWork(session) as uow:
            await self.org_repo.add_delete_utc(organization_id, delete_utc, uow.session)
