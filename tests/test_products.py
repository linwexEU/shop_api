from httpx import AsyncClient
import pytest
from unittest.mock import MagicMock, patch

from tests.clients.products import ProductsCli
from src.models.enums import CategoriesEnum


# Declare clients
products_cli = ProductsCli()


class TestProducts: 
    @pytest.mark.parametrize("caterogy,total_count", [
        (CategoriesEnum.Computers, 0), (CategoriesEnum.Monitors, 1), (CategoriesEnum.Keyboards, 1)
    ])
    async def test_get_all_products(self, caterogy: CategoriesEnum, total_count: int, ac: AsyncClient): 
        pagination = {"offset": 0, "limit": 60}

        products = await products_cli.get_all_products(caterogy, pagination, ac)
        assert products.TotalCount == total_count

    async def test_product_rates(self, customer_ac: AsyncClient): 
        # Add rate to product
        data = {"stars": 5}
        rate_id = (await products_cli.add_rate_to_product(1, data, customer_ac)).rate_id
        
        assert rate_id == 1 

        # Get product rates 
        rates = await products_cli.get_product_rates(1, customer_ac)
        assert rates.TotalCount == 1

    async def test_rate_replies(self, customer_ac: AsyncClient): 
        # Add rate to product
        data = {"stars": 5}
        rate_id = (await products_cli.add_rate_to_product(1, data, customer_ac)).rate_id
        
        assert rate_id == 1 

        # Get product rates 
        rates = await products_cli.get_product_rates(1, customer_ac)
        assert rates.TotalCount == 1 

        # Add reply to rate 
        data = {"text": "Overrated!"}
        reply_id = (await products_cli.add_reply_to_rate(rate_id, data, customer_ac)).reply_id

        assert reply_id == 1 

        # Get replies for Rate 
        replies = await products_cli.get_rate_replies(rate_id, customer_ac)
        assert replies.TotalCount == 1

        # Check reply data 
        reply = replies.Data[0] 

        assert reply.text == data["text"]

    async def test_likes_and_dislikes(self, customer_ac: AsyncClient, owner_ac: AsyncClient): 
        product_id = 1 

        # Add rate to product(id = 1)
        data = {
            "stars": 4, 
            "notes": "Nice product!"
        }
        rate_id = (await products_cli.add_rate_to_product(product_id, data, customer_ac)).rate_id

        # Get product(id=1) rates
        rates = await products_cli.get_product_rates(product_id, customer_ac)

        assert rates.TotalCount == 1
        assert rates.Data[0].stars == 4
        assert rates.Data[0].likes == 0
        assert rates.Data[0].dislikes == 0
        
        # Like rate (same user) 
        response = await products_cli.like_rate(rate_id, customer_ac)
        assert response.status_code == 404 

        # Like rate (another user) 
        rate_id = (await products_cli.like_rate(rate_id, owner_ac)).rate_id 

        # Get product(id=1) rates
        await self.check_likes_and_dislikes(product_id, 1, 0, customer_ac)

        # Remove like and dislike post 
        rate_id = (await products_cli.dislike_rate(rate_id, owner_ac)).rate_id 

        # Get product(id=1) rates
        await self.check_likes_and_dislikes(product_id, 0, 1, customer_ac)

    @patch("src.products.flow.add_products_background.delay")
    async def test_add_products(self, mock_bg_task: MagicMock, owner_ac: AsyncClient): 
        mock_bg_task.return_value = True
        organization_id = 1 

        # Check message
        message = (await products_cli.add_products(organization_id, "monitors.xlsx", owner_ac)).message
        assert message == "Your products are adding..."

        # Check that add_products_background.delay was called
        mock_bg_task.assert_called_once()

    @patch("src.products.flow.add_products_background.delay")
    async def test_add_products_with_no_owner_permission(self, mock_bg_task: MagicMock, customer_ac: AsyncClient): 
        mock_bg_task.return_value = True
        organization_id = 1 

        response = await products_cli.add_products(organization_id, "monitors.xlsx", customer_ac)
        assert response.status_code == 403
        assert response.json()["detail"] == "Only Owner access"

    @patch("src.products.flow.add_products_background.delay")
    async def test_add_products_with_another_organization_id(self, mock_bg_task: MagicMock, owner_ac: AsyncClient): 
        mock_bg_task.return_value = True 
        organization_id = 3 

        response = await products_cli.add_products(organization_id, "monitors.xlsx", owner_ac) 
        assert response.status_code == 403 
        assert response.json()["detail"] == "Not Your Organization"

    @patch("src.products.flow.add_products_background.delay")
    async def test_add_products_with_not_excel_file(self, mock_bg_task: MagicMock, owner_ac: AsyncClient): 
        mock_bg_task.retur_value = True 
        organization_id = 1 

        response = await products_cli.add_products(organization_id, "not_excel.txt", owner_ac) 
        assert response.status_code == 400 
        assert response.json()["detail"] == "Not Excel file"

    @staticmethod
    async def check_likes_and_dislikes(product_id: int, likes: int, dislikes: int, user: AsyncClient): 
        rates = await products_cli.get_product_rates(product_id, user)

        assert rates.Data[0].likes == likes
        assert rates.Data[0].dislikes == dislikes
