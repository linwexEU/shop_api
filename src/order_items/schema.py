from pydantic import BaseModel 


class SOrderItemsModel(BaseModel): 
    order_id: int
    product_id: int
    user_id: int
    quantity: int


class SOrderItemsFilters(BaseModel): 
    order_id: int | None = None 
    product_id: int | None = None
