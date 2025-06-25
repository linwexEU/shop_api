from httpx import AsyncClient, Response

from src.models.enums import OrdersStateChangerEnum
from src.orders.schema import SOrderResult, SOrdersPayload



class OrdersCli: 
    def url(self, postfix: str) -> str: 
        prefix = "/orders" 
        return f"{prefix}{postfix}"
    
    async def get_orders(self, ac: AsyncClient) -> SOrdersPayload | Response: 
        url = self.url("/")
        response = await ac.get(url) 

        if response.status_code == 200: 
            return SOrdersPayload(**response.json()) 
        return response 
    
    async def make_order(self, ac: AsyncClient) -> SOrderResult | Response: 
        url = self.url("/make-order")
        response = await ac.post(url) 

        if response.status_code == 200: 
            return SOrderResult(**response.json()) 
        return response 
    
    async def change_order_state(self, uuid: str, state: OrdersStateChangerEnum, ac: AsyncClient) -> None | Response: 
        url = self.url(f"/{uuid}/state/{state}")
        response = await ac.patch(url) 

        if response.status_code != 204: 
            return response
