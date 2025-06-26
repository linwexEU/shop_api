from src.models.models import Users
from src.db.db import AsyncSessionDep
from src.users.repository import PersistenceUsersRepository
from src.users.schema import SUsersFilters, SUsersModel
from src.utils.uow import UnitOfWork


class UsersService:
    def __init__(self, users_repo: PersistenceUsersRepository):
        self.users_repo: PersistenceUsersRepository = users_repo()

    async def add(self, data: SUsersModel, session: AsyncSessionDep) -> int:
        async with UnitOfWork(session) as uow:
            return await self.users_repo.add(data.model_dump(), uow.session)

    async def get_by_filters(self, filters: SUsersFilters, session: AsyncSessionDep, one: bool = True) -> Users | list[Users]:
        return await self.users_repo.get_by_filters(filters.model_dump(exclude_none=True), session, one)

    async def get_or_create(self, data: SUsersModel, session: AsyncSessionDep):
        async with UnitOfWork(session) as uow:
            return await self.users_repo.get_or_create(data.model_dump(), uow.session)

    async def get_organizations(self, owner_id: int, session: AsyncSessionDep):
        return await self.users_repo.get_organizations(owner_id, session)
