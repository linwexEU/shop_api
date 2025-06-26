from src.models.models import ProductRatesInteraction
from src.db.db import AsyncSessionDep
from src.product_rates_interaction.repository import PersistenceProductRatesInteractionRepository
from src.product_rates_interaction.schema import SLikedProductRateFilters, SLikedProductRateModel
from src.utils.uow import UnitOfWork


class ProductRatesInteractionService:
    def __init__(self, liked_repo: PersistenceProductRatesInteractionRepository):
        self.liked_repo: PersistenceProductRatesInteractionRepository = liked_repo()

    async def add(self, data: SLikedProductRateModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.liked_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SLikedProductRateFilters, session: AsyncSessionDep, one: bool = True) -> list[ProductRatesInteraction] | ProductRatesInteraction:
        return await self.liked_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)
