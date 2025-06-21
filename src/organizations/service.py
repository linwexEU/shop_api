from datetime import datetime

from src.organizations.repository import OrganizationsRepository
from src.organizations.schema import SOrganizationsFilters, SOrganizationsModel


class OrganizationsService:
    def __init__(self, org_repo: OrganizationsRepository):
        self.org_repo: OrganizationsRepository = org_repo()

    async def add(self, data: SOrganizationsModel) -> int:
        return await self.org_repo.add(data.model_dump())

    async def get_all(self):
        return await self.org_repo.get_all()

    async def get_by_filters(self, filters: SOrganizationsFilters):
        return await self.org_repo.get_by_filters(filters.model_dump(exclude_none=True))

    async def delete_by_id(self, entity_id: int) -> int:
        return await self.org_repo.delete_by_id(entity_id)

    async def add_delete_utc(self, organization_id: int, delete_utc: datetime) -> None:
        await self.org_repo.add_delete_utc(organization_id, delete_utc)
