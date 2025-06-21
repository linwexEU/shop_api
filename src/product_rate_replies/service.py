from src.product_rate_replies.schema import SProductRateReplies, SProductRateRepliesFilters
from src.product_rate_replies.repository import ProductRateRepliesRepository 


class ProductRateRepliesService: 
    def __init__(self, replies_repo: ProductRateRepliesRepository): 
        self.replies_repo: ProductRateRepliesRepository = replies_repo()

    async def add(self, data: SProductRateReplies) -> int: 
        return await self.replies_repo.add(data.model_dump()) 
    
    async def get_by_filters(self, filters: SProductRateRepliesFilters, one: bool = True): 
        return await self.replies_repo.get_by_filters(filters.model_dump(exclude_none=True), one)
