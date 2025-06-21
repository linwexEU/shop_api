import asyncio
import logging

import orjson
from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage

from src.config import settings
from src.logger import config_logger
from src.products.schema import SProductsModel
from src.products.service import ProductsService
from src.utils.dependency import products_service

logger = logging.getLogger(__name__)

# Configure logger
config_logger()


class Consumer:
    async def connect(self) -> None:
        # Perform connection
        self.connection = await connect(settings.RABBITMQ_URL)

        logger.info("RabbitMQ start...")

    async def initialize(self) -> None:
        # Creating an exchange
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        # Declare an exchange
        self.topic_db_exchange = await self.channel.declare_exchange(
            "topic_db", ExchangeType.TOPIC
        )

        # Declare queue
        self.queue = await self.channel.declare_queue("task_queue", durable=True)
        await self.queue.bind(self.topic_db_exchange, routing_key="db")

    @staticmethod
    def deserialize(message: bytes) -> dict:
        return orjson.loads(message)

    async def receive_messages(self) -> None:
        products_service_db: ProductsService = products_service()
        while True:
            try:
                # Start listening the queue with name 'task_queue'
                async with self.queue.iterator() as iterator:
                    message: AbstractIncomingMessage
                    async for message in iterator:
                        async with message.process(requeue=True):
                            product_data = self.deserialize(message.body)

                            # Add product data to DB
                            await products_service_db.add(
                                SProductsModel(**product_data)
                            )

                            logger.info(
                                f"RabbitMQ: Product(title={product_data['title']}) added!"
                            )
            except Exception as ex:
                logger.error("RabbitMQ error: %s" % ex)


async def main() -> None:
    consumer = Consumer()
    await consumer.connect()
    await consumer.initialize()
    await consumer.receive_messages()


if __name__ == "__main__":
    asyncio.run(main())
