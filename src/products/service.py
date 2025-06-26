from src.models.models import Products
from src.db.db import AsyncSessionDep
from src.models.enums import CategoriesEnum
from src.products.repository import PersistenceProductsRepository
from src.products.schema import (SProductFilters, SProductsModel,
                                 SProductsSearch)
from src.utils.uow import UnitOfWork


class ProductsService:
    def __init__(self, prod_repo: PersistenceProductsRepository):
        self.prod_repo: PersistenceProductsRepository = prod_repo()

    async def add(self, data: SProductsModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.prod_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SProductFilters, session: AsyncSessionDep, one: bool = True) -> list[Products] | Products:
        return await self.prod_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one) 
    
    async def get_product_count(self, category: CategoriesEnum, session: AsyncSessionDep) -> int:
        return await self.prod_repo.get_product_count(category, session)

    async def get_products_by_search(self, search: SProductsSearch, category: CategoriesEnum, session: AsyncSessionDep):
        return await self.prod_repo.get_products_by_search(search, category, session)
