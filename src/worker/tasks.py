from src.broker.producer import Producer
from src.db.db import async_session_maker
from src.models.enums import CategoriesEnum, NotificationsTypeEnum
from src.notifications.schema import SNotifications
from src.scripts.generator import GenerateExcel, ReadExcel
from src.scripts.parser import run_script
from src.utils.dependency import notifications_service
from src.worker.app import async_celery
from src.worker.ses import SESClient


@async_celery.task
async def fill_db_products(category: CategoriesEnum) -> None:
    await run_script(category)


@async_celery.task
async def add_products_background(organization_id: int, excel_file: bytes) -> None:
    # Read data from excel_file
    read_excel = ReadExcel(excel_file)
    data = read_excel.read_file()

    # Add products
    for item in data:
        item.update({"organization_id": organization_id})

        async with Producer() as producer:
            await producer.send_message(item)


@async_celery.task
async def send_products_list(to: str, from_: str, subject: str, body: str, data: list):
    # Create generator instance
    generator = GenerateExcel()

    # Headings
    headings = ["title", "price", "image", "quantity"]

    # Generate excel file
    excel_file = generator.generate_file_buffer(headings, data)

    # Send email
    ses_clinet = SESClient()
    ses_clinet.send_email_with_attachment(
        to,
        from_,
        subject,
        body,
        attachment=excel_file.getvalue(),
        filename="Basket.xlsx",
    )


@async_celery.task
async def send_notification(target_id: int, type: NotificationsTypeEnum):
    notifications_service_db = notifications_service()

    # Send notification
    async with async_session_maker() as session:
        await notifications_service_db.add(SNotifications(type=type, user_id=target_id), session)
