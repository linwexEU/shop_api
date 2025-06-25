from httpx import AsyncClient

from tests.clients.baskets import BasketsCli 
from tests.clients.orders import OrdersCli 
from src.models.enums import OrdersStateChangerEnum


orders_cli = OrdersCli() 
baskets_cli = BasketsCli() 


class TestOrders: 
    async def test_get_order(self, customer_ac: AsyncClient): 
        # Add products to basket
        product1_id = 1 
        product2_id = 2

        for _ in range(2):
            await baskets_cli.add_product_to_basket(product1_id, customer_ac) 
        
        await baskets_cli.add_product_to_basket(product2_id, customer_ac) 

        # Check basket  
        products = await baskets_cli.get_products_from_basket(customer_ac)

        assert len(products.Data) == 2 

        assert products.Data[0].product.id == product1_id
        assert products.Data[1].product.id == product2_id 

        assert products.Data[0].quantity == 2 
        assert products.Data[1].quantity == 1 

        # Make order 
        orders = await orders_cli.get_orders(customer_ac)
        assert len(orders.Data) == 0

        order = await orders_cli.make_order(customer_ac) 
        assert order is not None 

        # Check our order with two products
        orders = await orders_cli.get_orders(customer_ac)
        assert len(orders.Data) == 1
        assert len(orders.Data[0].products) == 2

    async def test_check_order_states(self, customer_ac: AsyncClient, admin_ac: AsyncClient): 
        # Add products to basket
        product1_id = 1 
        product2_id = 2

        for _ in range(2):
            await baskets_cli.add_product_to_basket(product1_id, customer_ac) 
        
        await baskets_cli.add_product_to_basket(product2_id, customer_ac) 

        # Check basket  
        products = await baskets_cli.get_products_from_basket(customer_ac)

        assert len(products.Data) == 2 

        assert products.Data[0].product.id == product1_id
        assert products.Data[1].product.id == product2_id 

        assert products.Data[0].quantity == 2 
        assert products.Data[1].quantity == 1 

        # Make order 
        orders = await orders_cli.get_orders(customer_ac)
        assert len(orders.Data) == 0

        order = await orders_cli.make_order(customer_ac) 
        assert order is not None 

        # Check our order with two products
        orders = await orders_cli.get_orders(customer_ac)
        assert len(orders.Data) == 1
        assert len(orders.Data[0].products) == 2

        # Test Machine State 
        order_uuid = orders.Data[0].uuid 
        
        # Try to Done without Delivering 
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Done.value, admin_ac)
        assert response.status_code == 409 
        assert response.json()["detail"] == f"Invalid state transition from '{orders.Data[0].state.value}'"

        # Delivering
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Delivering.value, admin_ac) 
        assert response is None 

        # Done 
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Done.value, admin_ac) 
        assert response is None 

        # Update orders 
        orders = await orders_cli.get_orders(customer_ac)

        # Canceled 
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Canceled.value, admin_ac) 
        assert response.status_code == 409 
        assert response.json()["detail"] == f"Invalid state transition from '{orders.Data[0].state.value}'"

        # Make another order 
        order = await orders_cli.make_order(customer_ac) 
        assert order is not None 

        # Update orders 
        orders = await orders_cli.get_orders(customer_ac)

        order_uuid = orders.Data[1].uuid

        # Canceled 
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Canceled.value, admin_ac) 
        assert response is None 

        # Done 
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Done.value, admin_ac) 
        assert response.status_code == 409

        # Delivering 
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Delivering.value, admin_ac) 
        assert response.status_code == 409  

        # Not admin  
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Delivering.value, customer_ac) 
        assert response.status_code == 403 
