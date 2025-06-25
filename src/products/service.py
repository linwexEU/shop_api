from src.models.enums import CategoriesEnum
from src.products.repository import ProductsRepository
from src.products.schema import (SProductFilters, SProductsModel,
                                 SProductsSearch)


class ProductsService:
    def __init__(self, prod_repo: ProductsRepository):
        self.prod_repo: ProductsRepository = prod_repo()

    async def add(self, data: SProductsModel) -> int:
        return await self.prod_repo.add(data.model_dump())

    async def get_all(self):
        return await self.prod_repo.get_all()

    async def get_by_filters(self, filters: SProductFilters, one: bool = True):
        return await self.prod_repo.get_by_filters(
            filters.model_dump(exclude_none=True), one
        )

    async def delete_by_id(self, entity_id: int) -> int:
        return await self.prod_repo.delete_by_id(entity_id)

    async def get_product_count(self, category: CategoriesEnum) -> int:
        return await self.prod_repo.get_product_count(category)

    async def get_products_by_search(
        self, search: SProductsSearch, category: CategoriesEnum
    ):
        return await self.prod_repo.get_products_by_search(search, category)
