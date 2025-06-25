from src.categories.repository import CategoriesRepository
from src.categories.schema import SCategoriesFilters, SCategoriesModel


class CategoriesService(CategoriesRepository):
    def __init__(self, cater_repo: CategoriesRepository):
        self.cater_repo: CategoriesRepository = cater_repo()

    async def add(self, data: SCategoriesModel) -> int:
        return await self.cater_repo.add(data.model_dump())

    async def get_all(self):
        return await self.cater_repo.get_all()

    async def get_by_filters(self, filters: SCategoriesFilters, one: bool = True):
        return await self.cater_repo.get_by_filters(
            filters.model_dump(exclude_none=True), one
        )

    async def delete_by_id(self, entity_id: int) -> int:
        return await self.cater_repo.delete_by_id(entity_id)
