from httpx import AsyncClient, Response

from src.organization_rates.schema import SOrganizationRateAddResponse, SOrganizationRatesResponse
from src.organizations.schema import SOrganizationAddResponse, SOrganizationDeleteResponse, SOrganizationResponse


class OrganizationsCli: 
    def url(self, postfix): 
        prefix = "/organizations"
        return f"{prefix}{postfix}"
    
    async def get_organization(self, organization_id: int, ac: AsyncClient) -> SOrganizationResponse | Response: 
        url = self.url(f"/{organization_id}")
        response = await ac.get(url) 
        
        if response.status_code == 200: 
            return SOrganizationResponse(**response.json()) 
        return response 

    async def add_organization(self, data: dict, ac: AsyncClient) -> SOrganizationAddResponse | Response: 
        url = self.url("/add")
        response = await ac.post(url, json=data) 

        if response.status_code == 201: 
            return SOrganizationAddResponse(**response.json())
        return response 
    
    async def get_organization_rates(self, organization_id: int, ac: AsyncClient) -> SOrganizationRatesResponse | Response: 
        url = self.url(f"/{organization_id}/rates")
        response = await ac.get(url) 

        if response.status_code == 200: 
            return SOrganizationRatesResponse(**response.json())
        return response
    
    async def add_rate_to_organization(self, organization_id: int, data: dict, ac: AsyncClient) -> SOrganizationRateAddResponse | Response: 
        url = self.url(f"/{organization_id}/rates")
        response = await ac.post(url, json=data) 

        if response.status_code == 201: 
            return SOrganizationRateAddResponse(**response.json()) 
        return response

    async def delete_organization(self, organization_id: int, ac: AsyncClient) -> SOrganizationDeleteResponse | Response: 
        url = self.url(f"/{organization_id}")
        response = await ac.delete(url) 

        if response.status_code == 200: 
            return SOrganizationDeleteResponse(**response.json())
        return response
