from httpx import AsyncClient
from unittest.mock import MagicMock, patch

from tests.clients.baskets import BasketsCli 


baskets_cli = BasketsCli()


class TestBaskets: 
    async def test_add_product_to_basket(self, customer_ac: AsyncClient): 
        product1_id = 1 
        product2_id = 2

        # Add product to basket 
        await baskets_cli.add_product_to_basket(product1_id, customer_ac) 

        # Get user's basket 
        products = await baskets_cli.get_products_from_basket(customer_ac)
        assert len(products.Data) == 1 
        assert products.Data[0].product.id == product1_id

        # Add another product 
        await baskets_cli.add_product_to_basket(product2_id, customer_ac) 

        # Get user's basket 
        products = await baskets_cli.get_products_from_basket(customer_ac) 
        assert len(products.Data) == 2

    async def test_delete_product_from_basket(self, customer_ac: AsyncClient): 
        product_id = 1 

        # Add product to basket 
        for _ in range(3): 
            await baskets_cli.add_product_to_basket(product_id, customer_ac) 
        
        # Get user's basket 
        products = await baskets_cli.get_products_from_basket(customer_ac) 
        assert len(products.Data) == 1 
        assert products.Data[0].quantity == 3

        # Delete product
        await baskets_cli.delete_product_from_basket(product_id, customer_ac) 

        # Get user's basket 
        products = await baskets_cli.get_products_from_basket(customer_ac) 
        assert products.Data[0].quantity == 2 

        # Delete product full 
        await baskets_cli.delete_all_product_from_basket(product_id, customer_ac) 

        # Get user's basket 
        products = await baskets_cli.get_products_from_basket(customer_ac) 
        assert len(products.Data) == 0

    @patch("src.baskets.flow.send_products_list.delay")
    async def test_send_product_list_to_email(self, mock_sender: MagicMock, customer_ac: AsyncClient): 
        # Mock SES
        mock_sender.return_value = True

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
        assert products.Data[0].quantity == 2 

        assert products.Data[1].product.id == product2_id
        assert products.Data[1].quantity == 1

        # Send email list 
        response = await baskets_cli.send_products_list(customer_ac)
        assert response.message == "File was send to your email"

        # Clear basket 
        await baskets_cli.clear_all_products(customer_ac)

        # Send email list (Error due to empty basket)
        response = await baskets_cli.send_products_list(customer_ac)
        assert response.status_code == 400 
        assert response.json()["detail"] == "Your basket is empty"      
