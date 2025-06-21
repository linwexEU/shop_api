from src.product_rates.repository import ProductRatesRepository
from src.product_rates.schema import SProductRatesFilters, SProductRatesModel


class ProductRatesService:
    def __init__(self, prod_rates_repo: ProductRatesRepository):
        self.prod_rates_repo: ProductRatesRepository = prod_rates_repo()

    async def add(self, data: SProductRatesModel) -> int:
        return await self.prod_rates_repo.add(data.model_dump())

    async def get_all(self):
        return await self.prod_rates_repo.get_all()

    async def get_by_filters(self, filters: SProductRatesFilters, one: bool = True):
        return await self.prod_rates_repo.get_by_filters(
            filters.model_dump(exclude_none=True), one
        )

    async def delete_by_id(self, entity_id: int) -> int:
        return await self.prod_rates_repo.delete_by_id(entity_id)

    async def like_rate(self, rate_id: int, user_id: int) -> int:
        return await self.prod_rates_repo.like_rate(rate_id, user_id)

    async def dislike_rate(self, rate_id: int, user_id: int) -> int:
        return await self.prod_rates_repo.dislike_rate(rate_id, user_id)

    async def remove_like_rate(self, rate_id: int) -> int:
        return await self.prod_rates_repo.remove_like_rate(rate_id)

    async def remove_dislike_rate(self, rate_id: int) -> int:
        return await self.prod_rates_repo.remove_dislike_rate(rate_id)
