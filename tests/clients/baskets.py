from httpx import AsyncClient, Response

from src.baskets.schema import SBasket, SBasketDeleteResponse, SBasketExcelResponse, SBasketPayload, SBasketResponse 


class BasketsCli: 
    def url(self, postfix: str) -> str: 
        prefix = "/baskets"
        return f"{prefix}{postfix}"
    
    async def get_products_from_basket(self, ac: AsyncClient) -> SBasketPayload | Response: 
        url = self.url("/")
        response = await ac.get(url) 

        if response.status_code == 200:
            return SBasketPayload(**response.json())
        return response
    
    async def add_product_to_basket(self, product_id: int, ac: AsyncClient) -> SBasketResponse | Response: 
        url = self.url(f"/add/{product_id}")
        response = await ac.post(url) 

        if response.status_code == 200: 
            return SBasketResponse(**response.json())
        return response
    
    async def delete_product_from_basket(self, product_id: int, ac: AsyncClient) -> SBasketDeleteResponse | Response: 
        url = self.url(f"/delete/{product_id}")
        response = await ac.delete(url) 

        if response.status_code == 200: 
            return SBasketDeleteResponse(**response.json())
        return response 

    async def delete_all_product_from_basket(self, product_id: int, ac: AsyncClient) -> SBasketDeleteResponse: 
        url = self.url(f"/delete/{product_id}/all")
        response = await ac.delete(url) 

        if response.status_code == 200: 
            return SBasketDeleteResponse(**response.json())
        return response

    async def clear_all_products(self, ac: AsyncClient) -> None | Response: 
        url = self.url("/clear")
        response = await ac.delete(url) 

        if response.status_code != 204: 
            return response
        
    async def send_products_list(self, ac: AsyncClient) -> SBasketExcelResponse | Response: 
        url = self.url("/send-list")
        response = await ac.post(url) 

        if response.status_code == 200: 
            return SBasketExcelResponse(**response.json())
        return response
