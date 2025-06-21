from pydantic import BaseModel

from src.models.enums import OrdersStateEnum
from src.models.models import OrderItems


class SOrdersModel(BaseModel):
    uuid: str
    total_price: float
    user_id: int


class SOrdersFilters(BaseModel):
    uuid: str | None = None
    state: OrdersStateEnum | None = None
    user_id: int | None = None


class SProductFromOrder(BaseModel):
    title: str
    image: str
    price: float
    quantity: int


class SOrders(BaseModel):
    uuid: str
    state: OrdersStateEnum
    products: list[SProductFromOrder]
    total_price: float


class SOrdersPayload(BaseModel):
    TotalCount: int
    Data: list[SOrders]


class SOrderResult(BaseModel):
    order_id: int
