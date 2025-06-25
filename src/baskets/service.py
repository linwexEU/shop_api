from src.baskets.repository import BasketsRepository
from src.baskets.schema import SBasketsFilters, SBasketsModel


class BasketsService:
    def __init__(self, bask_repo: BasketsRepository):
        self.bask_repo: BasketsRepository = bask_repo()

    async def add(self, data: SBasketsModel) -> int:
        return await self.bask_repo.add(data.model_dump())

    async def get_all(self):
        return await self.bask_repo.get_all()

    async def get_by_filters(self, filters: SBasketsFilters, one: bool = True):
        return await self.bask_repo.get_by_filters(
            filters.model_dump(exclude_none=True), one
        )

    async def delete_by_id(self, entity_id: int) -> int:
        return await self.bask_repo.delete_by_id(entity_id)

    async def get_basket_with_products(self, user_id: int):
        return await self.bask_repo.get_basket_with_products(user_id)

    async def increase_item_count(self, product_id: int, user_id: int) -> int:
        return await self.bask_repo.increase_item_count(product_id, user_id)

    async def decrease_item_count(self, product_id: int, user_id: int) -> int:
        return await self.bask_repo.decrease_item_count(product_id, user_id)

    async def delete_product(self, product_id: int, user_id: int) -> int:
        return await self.bask_repo.delete_product(product_id, user_id)

    async def clear_basket(self, user_id: int) -> None:
        await self.bask_repo.clear_basket(user_id)
