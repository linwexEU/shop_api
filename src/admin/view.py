from fastapi import APIRouter, status

from src.auth.dependencies import AdminUserDep
from src.models.enums import CategoriesEnum
from src.worker.tasks import fill_db_products

router = APIRouter()


@router.post("/fill/{category}", status_code=status.HTTP_204_NO_CONTENT)
async def fill_db(category: CategoriesEnum, admin_user: AdminUserDep) -> None:
    # Send task to Celery
    fill_db_products.delay(category.value)
