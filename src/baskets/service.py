from src.models.models import Baskets
from src.baskets.repository import PersistenceBasketsRepository
from src.baskets.schema import SBasketsFilters, SBasketsModel
from src.db.db import AsyncSessionDep 
from src.utils.uow import UnitOfWork


class BasketsService:
    def __init__(self, bask_repo: PersistenceBasketsRepository):
        self.bask_repo: PersistenceBasketsRepository = bask_repo()

    async def add(self, data: SBasketsModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.bask_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SBasketsFilters, session: AsyncSessionDep, one: bool = True) -> list[Baskets] | Baskets:
        return await self.bask_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)

    async def get_basket_with_products(self, user_id: int, session: AsyncSessionDep):
        return await self.bask_repo.get_basket_with_products(user_id, session)

    async def increase_item_count(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.bask_repo.increase_item_count(product_id, user_id, uow.session)

    async def decrease_item_count(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.bask_repo.decrease_item_count(product_id, user_id, uow.session)

    async def delete_product(self, product_id: int, user_id: int, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.bask_repo.delete_product(product_id, user_id, uow.session)

    async def clear_basket(self, user_id: int, session: AsyncSessionDep) -> None:
        async with UnitOfWork(session) as uow:
            await self.bask_repo.clear_basket(user_id, uow.session)
