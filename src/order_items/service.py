from src.order_items.repository import OrderItemsRepository
from src.order_items.schema import SOrderItemsFilters, SOrderItemsModel


class OrderItemsService:
    def __init__(self, order_items_repo: OrderItemsRepository):
        self.order_items_repo: OrderItemsRepository = order_items_repo()

    async def add(self, data: SOrderItemsModel) -> int:
        return await self.order_items_repo.add(data.model_dump())

    async def get_all(self):
        return await self.order_items_repo.get_all()

    async def get_by_filters(self, filters: SOrderItemsFilters):
        return await self.order_items_repo.get_by_filters(
            filters.model_dump(exclude_none=True)
        )

    async def delete(self, entity_id: int) -> int:
        return await self.order_items_repo.delete_by_id(entity_id)

    async def get_full_order_items(self, user_id: int) -> int:
        return await self.order_items_repo.get_full_order_items(user_id)
