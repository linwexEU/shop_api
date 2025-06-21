from src.products.schema import SProductFilters, SProductsSearch
from src.models.models import Products 
from src.utils.repository import SQLAlchemyRepository 
from src.models.enums import CategoriesEnum
from src.db.db import async_session_maker 
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload


class ProductsRepository(SQLAlchemyRepository): 
    model = Products

    async def get_product_count(self, category: CategoriesEnum) -> int: 
        async with async_session_maker() as session: 
            query = select(func.count()).select_from(self.model).where(self.model.category == category) 
            result = await session.execute(query) 
            return result.scalar() 
        
    async def get_products_by_search(self, search: SProductsSearch, category: CategoriesEnum): 
        async with async_session_maker() as session: 
            query = select(self.model).where(self.model.category == category)
            
            if search.title: 
                query = query.where(self.model.title.ilike(f"%{search.title}%"))

            if search.low_price and search.high_price: 
                query = query.where(self.model.price.between(search.low_price, search.high_price))

            if search.desc_price: 
                query = query.order_by(self.model.price.desc())
            
            if search.asc_price: 
                query = query.order_by(self.model.price) 

            result = await session.execute(query) 
            return result.scalars().all()
