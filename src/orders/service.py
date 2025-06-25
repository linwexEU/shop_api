from src.models.enums import OrdersStateEnum
from src.orders.repository import OrdersRepository
from src.orders.schema import SOrdersFilters, SOrdersModel


class OrdersService:
    def __init__(self, orders_repo: OrdersRepository):
        self.orders_repo: OrdersRepository = orders_repo()

    async def add(self, data: SOrdersModel) -> int:
        return await self.orders_repo.add(data.model_dump())

    async def get_all(self):
        return await self.orders_repo.get_all()

    async def get_by_filters(self, filters: SOrdersFilters):
        return await self.orders_repo.get_by_filters(
            filters.model_dump(exclude_none=True)
        )

    async def delete_by_id(self, entity_id: int) -> int:
        return await self.orders_repo.delete_by_id(entity_id)

    async def update_state(self, uuid: int, state: OrdersStateEnum) -> int:
        return await self.orders_repo.update_state(uuid, state)

    async def canceled_order(self, uuid: str) -> int:
        return await self.orders_repo.canceled_order(uuid)
