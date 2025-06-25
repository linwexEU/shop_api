from httpx import AsyncClient

from tests.clients.notifications import NotificationsCli 
from tests.clients.baskets import BasketsCli 
from tests.clients.orders import OrdersCli

from src.utils.dependency import notifications_service
from src.models.enums import NotificationsTypeEnum, OrdersStateChangerEnum
from src.notifications.schema import SNotifications


notifications_cli = NotificationsCli() 
baskets_cli = BasketsCli() 
orders_cli = OrdersCli() 


class TestNotifications: 
    async def test_notifications(self, customer_ac: AsyncClient, admin_ac: AsyncClient): 
        # Init notifications service 
        notifications_service_db = notifications_service()

        # Products ids 
        product1_id = 1 
        product2_id = 2 

        # Add products to basket 
        for _ in range(2):
            await baskets_cli.add_product_to_basket(product1_id, customer_ac)
        await baskets_cli.add_product_to_basket(product2_id, customer_ac) 

        # Check basket 
        basket = await baskets_cli.get_products_from_basket(customer_ac) 
        assert len(basket.Data) == 2 

        # Make order 
        await orders_cli.make_order(customer_ac) 

        # Get order uuid 
        orders = await orders_cli.get_orders(customer_ac) 
        order_uuid = orders.Data[0].uuid 
        assert order_uuid is not None

        # Change order state 

        # Delivering
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Delivering.value, admin_ac)
        assert response is None 

        # Done 
        response = await orders_cli.change_order_state(order_uuid, OrdersStateChangerEnum.Done.value, admin_ac)
        assert response is None 

        # Create Notification 
        await notifications_service_db.add(
            SNotifications(
                type=NotificationsTypeEnum.NewOrder, 
                user_id=3 # customer_ac
            )
        )

        # Get notification 
        notifications = await notifications_cli.get_all_notifications(customer_ac) 
        assert notifications.NewCount == 1

        # Read notification(another user) 
        response = await notifications_cli.mark_as_read(notifications.Data[0].id, admin_ac) 
        assert response.status_code == 403 
        assert response.json()["detail"] == "Not your notification"

        # Read notification 
        notification_id = await notifications_cli.mark_as_read(notifications.Data[0].id, customer_ac) 
        assert notification_id is not None 

        # Check that we read notification 
        notifications = await notifications_cli.get_all_notifications(customer_ac) 
        assert notifications.NewCount == 0
