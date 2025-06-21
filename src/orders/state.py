import asyncio

from transitions import Machine, State
from src.models.enums import OrdersStateEnum
from src.utils.dependency import OrdersServiceDep 


class OrdersStateMachine: 
    def __init__(self, order_uuid: str, orders_service: OrdersServiceDep, current_state: OrdersStateEnum) -> None: 
        # Initialize states 
        self.states = [
            State(OrdersStateEnum.Preparing), 
            State(OrdersStateEnum.Delivering), 
            State(OrdersStateEnum.Done), 
            State(OrdersStateEnum.Canceled)
        ]

        # Initialize transitions
        self.transitions = [
            {"trigger": "prepared", "source": self.states[0], "dest": self.states[1], "after": ["change_state_sync"]}, 
            {"trigger": "delivered", "source": self.states[1], "dest": self.states[2], "after": ["change_state_sync"]}, 
            {"trigger": "canceled", "source": self.states[0], "dest": self.states[3], "after": ["canceled_order_syns"]}
        ]

        # Initialize machine
        self.machine = Machine(model=self, states=self.states, transitions=self.transitions, initial=current_state)
        self.order_uuid = order_uuid 
        self.orders_service = orders_service

    def change_state_sync(self):
        asyncio.create_task(self.change_state()) 

    def canceled_order_syns(self): 
        asyncio.create_task(self.canceled_order())

    async def change_state(self):
        match self.state: 
            case OrdersStateEnum.Delivering: 
                await self.orders_service.update_state(self.order_uuid, OrdersStateEnum.Delivering) 
            case OrdersStateEnum.Done: 
                await self.orders_service.update_state(self.order_uuid, OrdersStateEnum.Done)

    async def canceled_order(self):
        await self.orders_service.canceled_order(self.order_uuid)
