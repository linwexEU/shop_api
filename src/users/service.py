from src.users.repository import UsersRepository
from src.users.schema import SUsersFilters, SUsersModel


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo: UsersRepository = users_repo()

    async def add(self, data: SUsersModel) -> int:
        return await self.users_repo.add(data.model_dump())

    async def get_all(self):
        return await self.users_repo.get_all()

    async def get_by_filters(self, filters: SUsersFilters, one: bool = True):
        return await self.users_repo.get_by_filters(
            filters.model_dump(exclude_none=True), one
        )

    async def delete_by_id(self, entity_id: int) -> int:
        return await self.users_repo.delete_by_id(entity_id)

    async def get_or_create(self, data: SUsersModel):
        return await self.users_repo.get_or_create(data.model_dump())

    async def get_organizations(self, owner_id: int):
        return await self.users_repo.get_organizations(owner_id)
