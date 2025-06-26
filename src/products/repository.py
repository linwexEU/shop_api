from abc import ABC, abstractmethod

from sqlalchemy import func, select, insert

from src.db.db import AsyncSessionDep
from src.models.enums import CategoriesEnum
from src.models.models import Products
from src.products.schema import SProductsSearch


class ProductsReposiotory(ABC): 
    @abstractmethod
    async def add(self, data: dict, session: AsyncSessionDep) -> int: ...

    @abstractmethod 
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Products] | Products: ... 

    @abstractmethod 
    async def get_product_count(self, category: CategoriesEnum, session: AsyncSessionDep) -> int: ...

    @abstractmethod
    async def get_products_by_search(self, search: SProductsSearch, category: CategoriesEnum, session: AsyncSessionDep) -> list[Products]: ...


class PersistenceProductsRepository(ProductsReposiotory): 
    async def add(self, data: dict, session: AsyncSessionDep) -> int: 
        query = insert(Products).values(**data).returning(Products.id) 
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_by_filters(self, filters: dict, session: AsyncSessionDep, one: bool = True) -> list[Products] | Products: 
        query = select(Products).filter_by(**filters) 
        result = await session.execute(query) 

        if one: 
            return result.scalar() 
        return result.scalars().all()

    async def get_product_count(self, category: CategoriesEnum, session: AsyncSessionDep) -> int: 
        query = (
            select(func.count())
            .select_from(Products)
            .where(Products.category == category)
        )
        result = await session.execute(query) 
        return result.scalar() 
    
    async def get_products_by_search(self, search: SProductsSearch, category: CategoriesEnum, session: AsyncSessionDep) -> list[Products]: 
        query = select(Products).where(Products.category == category)

        if search.title: 
            query = query.where(Products.title.ilike(f"%{search.title}%"))

        if search.low_price and search.high_price: 
            query = query.where(Products.price.between(search.low_price, search.high_price))

        if search.desc_price:
            query = query.order_by(Products.price.desc())

        if search.asc_price:
            query = query.order_by(Products.price)

        result = await session.execute(query)
        return result.scalars().all()
