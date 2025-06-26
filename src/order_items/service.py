from src.db.db import AsyncSessionDep
from src.models.models import OrderItems
from src.order_items.repository import PersistenceOrderItemsRepository
from src.order_items.schema import SOrderItemsFilters, SOrderItemsModel
from src.utils.uow import UnitOfWork


class OrderItemsService:
    def __init__(self, order_items_repo: PersistenceOrderItemsRepository):
        self.order_items_repo: PersistenceOrderItemsRepository = order_items_repo()

    async def add(self, data: SOrderItemsModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.order_items_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SOrderItemsFilters, session: AsyncSessionDep, one: bool = True) -> list[OrderItems] | OrderItems:
        return await self.order_items_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)

    async def get_full_order_items(self, user_id: int, session: AsyncSessionDep) -> int:
        return await self.order_items_repo.get_full_order_items(user_id, session)
