import json
import asyncio

from httpx import AsyncClient, ASGITransport
from pathlib import Path
import pytest 
from sqlalchemy import insert
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.config import settings
from src.db.db import Base, async_session_maker, engine
from src.main import app as fastapi_app
from src.models.models import Users, Organizations, Products, OrganizationRates, ProductRateReplies, \
                            ProductRates, Baskets, Orders, OrderItems, Categories


pytest_plugins = ("pytest_asyncio", )


@pytest.fixture(autouse=True, scope="function")
async def prepare_database(): 
    assert settings.MODE == "TEST"

    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all) 

    def open_mock_json(model: str): 
        file_path = Path(__file__).parent / f"mock_json/mock_{model}.json"
        with open(file_path, encoding="utf-8") as file: 
            return json.load(file) 
    
    # Keep sequence
    users = open_mock_json("users") 
    organizations = open_mock_json("organizations") 
    products = open_mock_json("products")

    async with async_session_maker() as session: 
        for user in users:
            add_users = insert(Users).values(**user)
            await session.execute(add_users)

        for organization in organizations: 
            add_organizations = insert(Organizations).values(**organization) 
            await session.execute(add_organizations) 

        for product in products:
            add_products = insert(Products).values(**product) 
            await session.execute(add_products)

        await session.commit() 


@pytest.fixture(scope="session", autouse=True) 
async def init_test_cache(): 
    redis = aioredis.from_url(settings.REDIS_URL) 
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


# ac - async_client
@pytest.fixture(scope="function")
async def ac(): 
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac: 
        yield ac


@pytest.fixture(scope="session")
async def customer_ac(): 
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac: 
        await ac.post("/auth/", json={"email": "faddbs3@gmail.com", "password": "qwrtY1"})
        assert ac.cookies["access_token"] is not None
        yield ac


@pytest.fixture(scope="session")
async def admin_ac(): 
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac: 
        await ac.post("/auth/", json={"email": "linwexunstop@gmail.com", "password": "qwrtY1"})
        assert ac.cookies["access_token"] is not None
        yield ac


@pytest.fixture(scope="session") 
async def owner_ac(): 
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac: 
        await ac.post("/auth/", json={"email": "postertest0@gmail.com", "password": "qwrtY1"})
        assert ac.cookies["access_token"] is not None 
        yield ac


@pytest.fixture(scope="session")
def event_loop(request): 
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop() 
    yield loop 
    loop.close()
