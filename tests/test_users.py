import json

from httpx import AsyncClient
import pytest
from tests.clients.users import UsersCli
from unittest.mock import patch, MagicMock

from src.config import settings

# Declare clients
users_cli = UsersCli() 


class TestUsers:
    @patch("src.auth.flow.AuthFlow.validate_email")
    async def test_register_customer_user(self, mock_validate_email: MagicMock, ac: AsyncClient): 
        # Mock email verification
        mock_validate_email.return_value = True 

        data = {
            "username": "test_user", 
            "email": "test1@gmail.com", 
            "password": "qwrtY1", 
            "role": "Customer"
        }
        response = await users_cli.registration_user(data, ac)
        assert response.registered == True

    @patch("src.auth.flow.AuthFlow.validate_email")
    async def test_register_owner_user(self, mock_validate_email: MagicMock, ac: AsyncClient):
        # Mock email verification
        mock_validate_email.return_value = True

        data = {
            "username": "test_user2", 
            "email": "test2@gmail.com", 
            "password": "qwrtY1", 
            "role": "Owner"
        }
        response = await users_cli.registration_user(data, ac) 
        assert response.registered == True 

    @patch("src.auth.flow.AuthFlow.validate_email")
    async def test_register_admin_user(self, mock_validate_email: MagicMock, ac: AsyncClient): 
        # Mock verification email
        mock_validate_email.return_value = True

        data = {
            "username": "test_user3", 
            "email": "test3@gmail.com", 
            "password": "qwrtY1", 
            "role": "Admin", 
            "admin_token": settings.ADMIN_TOKEN
        }
        response = await users_cli.registration_user(data, ac) 
        assert response.registered == True

    @patch("src.auth.flow.AuthFlow.validate_email")
    async def test_register_admin_user_with_invalid_token(self, mock_validate: MagicMock, ac: AsyncClient): 
        # Mock verification email 
        mock_validate.return_value = True 

        data = {
            "username": "test_user3", 
            "email": "test3@gmail.com", 
            "password": "qwrtY1", 
            "role": "Admin", 
            "admin_token": "Incorrect token"
        }
        response = await users_cli.registration_user(data, ac) 
    
        assert response.status_code == 400
        assert json.loads(response.text).get("detail") == "Invalid AdminToken"

    @pytest.mark.parametrize("password", ["qwrtY1", "qwerwewe32"])
    async def test_auth_user(self, password: str, ac: AsyncClient): 
        data = {
            "email": "linwexunstop@gmail.com", 
            "password": password
        }

        response = await users_cli.auth_user(data, ac) 

        if password == "qwerwewe32": 
            assert response.status_code == 401
        else:
            assert response.access_token is not None
