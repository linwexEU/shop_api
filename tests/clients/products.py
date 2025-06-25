from httpx import AsyncClient, Response
from pathlib import Path

from src.product_rate_replies.schema import SProductRateRepliesModelResponse, SProductRateRepliesResult
from src.product_rates.schema import SRateDislikeResponse, SRateLikeResponse, SRatesModelResponse, SRatesResult
from src.products.schema import SProductAddResponse, SProductsResult
from src.models.enums import CategoriesEnum


class ProductsCli:
    def url(self, postfix: str) -> str: 
        prefix = "/products"
        return f"{prefix}{postfix}"
    
    # region Products

    async def get_all_products(self, category_type: CategoriesEnum, pagination: dict, ac: AsyncClient) -> SProductsResult | Response: 
        url = self.url(f"/{category_type.value}") 
        response = await ac.post(url, json=pagination)

        if response.status_code == 200:
            return SProductsResult(**response.json())
        
        return response
    
    async def add_products(self, organization_id: int, filename_with_ext: str, ac: AsyncClient) -> SProductAddResponse | Response: 
        url = self.url(f"/add/{organization_id}")

        # Load test excel file
        file_path = Path(__file__).parent.parent / f"files/{filename_with_ext}"
        files = {"excel_file": open(file_path, "rb")}

        response = await ac.post(url, files=files)

        if response.status_code == 201: 
            return SProductAddResponse(**response.json())
        return response
    
    # endregion Products 
    
    # region Rates

    async def get_product_rates(self, product_id: int, ac: AsyncClient) -> SRatesResult | Response: 
        url = self.url(f"/{product_id}/rates")
        response = await ac.get(url) 

        if response.status_code == 200: 
            return SRatesResult(**response.json())
        return response

    async def add_rate_to_product(self, product_id: int, data: dict, ac: AsyncClient) -> SRatesModelResponse | Response: 
        url = self.url(f"/{product_id}/rates")
        response = await ac.post(url, json=data)

        if response.status_code == 201: 
            return SRatesModelResponse(**response.json())
        return response 
    
    async def get_rate_replies(self, rate_id: int, ac: AsyncClient) -> SProductRateRepliesResult | Response: 
        url = self.url(f"/rates/{rate_id}/replies")
        response = await ac.get(url)

        if response.status_code == 200: 
            return SProductRateRepliesResult(**response.json())
        return response

    async def add_reply_to_rate(self, rate_id: int, data: dict, ac: AsyncClient) -> SProductRateRepliesModelResponse | Response: 
        url = self.url(f"/rates/{rate_id}/replies")
        response = await ac.post(url, json=data) 

        if response.status_code == 201: 
            return SProductRateRepliesModelResponse(**response.json())
        return response
    
    async def like_rate(self, rate_id: int, ac: AsyncClient) -> SRateLikeResponse | Response: 
        url = self.url(f"/rates/{rate_id}/like")
        response = await ac.patch(url)

        if response.status_code == 200: 
            return SRateLikeResponse(rate_id=rate_id)
        return response
    
    async def dislike_rate(self, rate_id: int, ac: AsyncClient) -> SRateDislikeResponse | Response: 
        url = self.url(f"/rates/{rate_id}/dislike")
        response = await ac.patch(url) 

        if response.status_code == 200: 
            return SRateDislikeResponse(rate_id=rate_id) 
        return response

    # endregion Rates
