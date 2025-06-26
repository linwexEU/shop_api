from src.models.models import Categories
from src.db.db import AsyncSessionDep
from src.categories.repository import PersistenceCategoriesRepository
from src.categories.schema import SCategoriesFilters, SCategoriesModel
from src.utils.uow import UnitOfWork


class CategoriesService:
    def __init__(self, cater_repo: PersistenceCategoriesRepository):
        self.cater_repo: PersistenceCategoriesRepository = cater_repo()

    async def add(self, data: SCategoriesModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.cater_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SCategoriesFilters, session: AsyncSessionDep, one: bool = True) -> list[Categories] | Categories:
        return await self.cater_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)
