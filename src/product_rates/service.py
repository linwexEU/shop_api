from src.models.models import ProductRates
from src.db.db import AsyncSessionDep
from src.product_rates.repository import PersistenceProductRatesRepository
from src.product_rates.schema import SProductRatesFilters, SProductRatesModel
from src.utils.uow import UnitOfWork


class ProductRatesService:
    def __init__(self, prod_rates_repo: PersistenceProductRatesRepository):
        self.prod_rates_repo: PersistenceProductRatesRepository = prod_rates_repo()

    async def add(self, data: SProductRatesModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.prod_rates_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SProductRatesFilters, session: AsyncSessionDep, one: bool = True) -> list[ProductRates] | ProductRates:
        return await self.prod_rates_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)

    async def like_rate(self, rate_id: int, user_id: int, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.prod_rates_repo.like_rate(rate_id, user_id, uow.session)

    async def dislike_rate(self, rate_id: int, user_id: int, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.prod_rates_repo.dislike_rate(rate_id, user_id, uow.session)

    async def remove_like_rate(self, rate_id: int, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.prod_rates_repo.remove_like_rate(rate_id, uow.session)

    async def remove_dislike_rate(self, rate_id: int, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.prod_rates_repo.remove_dislike_rate(rate_id, uow.session)
