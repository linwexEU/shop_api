from src.organization_rates.schema import SOrganizationRatesFilters, SOrganizationRatesModel
from src.organization_rates.repository import OrganizationRatesRepository 


class OgranizationRatesService: 
    def __init__(self, org_rates_repo: OrganizationRatesRepository): 
        self.org_rates_repo: OrganizationRatesRepository = org_rates_repo() 

    async def add(self, data: SOrganizationRatesModel) -> int: 
        return await self.org_rates_repo.add(data.model_dump()) 
    
    async def get_all(self): 
        return await self.org_rates_repo.get_all() 
    
    async def get_by_filters(self, filters: SOrganizationRatesFilters, one=True): 
        return await self.org_rates_repo.get_by_filters(filters.model_dump(exclude_none=True), one)
    
    async def delete_by_id(self, entity_id: int) -> int: 
        return await self.org_rates_repo.delete_by_id(entity_id)
