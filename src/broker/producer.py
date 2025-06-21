import asyncio
import logging
import orjson

from aio_pika import DeliveryMode, ExchangeType, Message, connect 

from src.logger import config_logger
from src.config import settings


logger = logging.getLogger(__name__) 

# Configure logger 
config_logger() 


class Producer: 
    async def connect(self) -> None: 
        self.connection = await connect(settings.RABBITMQ_URL)

    @staticmethod
    def serialize(message: dict) -> bytes: 
        return orjson.dumps(message)
    
    async def send_message(self, message: dict) -> None:
        try:
            async with self.connection: 
                channel = await self.connection.channel() 

                topic_db_exchange = await channel.declare_exchange(
                    "topic_db", ExchangeType.TOPIC
                )

                # Serialize mesage
                message_body = self.serialize(message)

                rabitt_message = Message(
                    message_body, 
                    delivery_mode=DeliveryMode.PERSISTENT
                )

                # Sent it
                await topic_db_exchange.publish(rabitt_message, routing_key="db")
                logger.info(f"RabbitMQ: Product(title={message['title']}) was sent to db")
        except Exception as ex:
            logger.error("RabbitMQ Error: %s" % ex)

    async def __aenter__(self) -> "Producer":
        await self.connect() 
        return self 
    
    async def __aexit__(self, exc_type, exc_value, traceback) -> None: 
        await self.connection.close()


async def main() -> None: 
    async with Producer() as producer:
        await producer.send_message({"category": "Computers", "title": "One Pc777", "price": 34533, "organization_id": 3, "image": "None"})


if __name__ == "__main__": 
    asyncio.run(main()) 
