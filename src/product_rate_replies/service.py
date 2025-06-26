from src.models.models import ProductRateReplies
from src.db.db import AsyncSessionDep
from src.product_rate_replies.repository import PersistenceProductRateRepliesRepository
from src.product_rate_replies.schema import SProductRateReplies, SProductRateRepliesFilters
from src.utils.uow import UnitOfWork


class ProductRateRepliesService:
    def __init__(self, replies_repo: PersistenceProductRateRepliesRepository):
        self.replies_repo: PersistenceProductRateRepliesRepository = replies_repo()

    async def add(self, data: SProductRateReplies, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.replies_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SProductRateRepliesFilters, session: AsyncSessionDep, one: bool = True) -> list[ProductRateReplies] | ProductRateReplies:
        return await self.replies_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)
