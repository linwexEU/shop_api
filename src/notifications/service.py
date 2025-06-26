from src.models.models import Notifications
from src.db.db import AsyncSessionDep
from src.notifications.repository import PersistenceNotificationsRepository
from src.notifications.schema import SNotifications, SNotificationsFilters
from src.utils.uow import UnitOfWork


class NotificationsService:
    def __init__(self, notifications_repo: PersistenceNotificationsRepository):
        self.notifications_repo: PersistenceNotificationsRepository = notifications_repo()

    async def add(self, data: SNotifications, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.notifications_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SNotificationsFilters, session: AsyncSessionDep, one: bool = True) -> list[Notifications] | Notifications:
        return await self.notifications_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)

    async def notification_checked(self, id: int, user_id: int, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.notifications_repo.notification_checked(id, user_id, uow.session)
