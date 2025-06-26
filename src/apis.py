from fastapi import APIRouter

from src.admin.view import router as admin_router
from src.auth.view import router as auth_router
from src.baskets.view import router as baskets_router
from src.notifications.view import router as notifications_router
from src.orders.view import router as orders_router
from src.organizations.view import router as organization_router
from src.products.view import router as product_router

api_router = APIRouter()


# Auth router
api_router.include_router(auth_router, prefix="/auth", tags=["Authenticate & Registration"])


# Admin router
api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])


# Product router
api_router.include_router(product_router, prefix="/products", tags=["Products"])


# Organization router
api_router.include_router(organization_router, prefix="/organizations", tags=["Organizations"])


# Basket router
api_router.include_router(baskets_router, prefix="/baskets", tags=["Baskets"])


# Orders router
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])


# Notifications router
api_router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
