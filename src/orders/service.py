from src.db.db import AsyncSessionDep
from src.models.enums import OrdersStateEnum
from src.models.models import Orders
from src.orders.repository import PersistenceOrdersRepository
from src.orders.schema import SOrdersFilters, SOrdersModel
from src.utils.uow import UnitOfWork


class OrdersService:
    def __init__(self, orders_repo: PersistenceOrdersRepository):
        self.orders_repo: PersistenceOrdersRepository = orders_repo()

    async def add(self, data: SOrdersModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.orders_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SOrdersFilters, session: AsyncSessionDep, one: bool = True) -> list[Orders] | Orders:
        return await self.orders_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)

    async def update_state(self, uuid: int, state: OrdersStateEnum, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow: 
            return await self.orders_repo.update_state(uuid, state, uow.session)

    async def canceled_order(self, uuid: str, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.orders_repo.canceled_order(uuid, uow.session)
