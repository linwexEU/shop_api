from src.product_rates_interaction.schema import SLikedProductRateModel, SLikedProductRateFilters
from src.product_rates_interaction.repository import ProductRatesInteractionRepository 


class ProductRatesInteractionService: 
    def __init__(self, liked_repo: ProductRatesInteractionRepository): 
        self.liked_repo: ProductRatesInteractionRepository = liked_repo() 

    async def add(self, data: SLikedProductRateModel) -> int: 
        return await self.liked_repo.add(data.model_dump()) 

    async def get_by_filters(self, filters: SLikedProductRateFilters, one: bool = True): 
        return await self.liked_repo.get_by_filters(filters.model_dump(exclude_none=True), one) 

    async def delete_by_id(self, entity_id: int) -> int: 
        return await self.liked_repo.delete_by_id(entity_id)  
