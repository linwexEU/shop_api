import asyncio
import logging
from functools import wraps
from typing import Coroutine

from src.logger import config_logger
from src.utils.exception import ParserExpcetion

logger = logging.getLogger(__name__)

# Configure logger
config_logger()


def async_retry(attempts_count: int, raise_exc: bool = True, delay: int = 1):
    def decorator(coroutine: Coroutine):
        @wraps(coroutine)
        async def wrapper(*args, **kwargs):
            free_attempts = attempts_count
            for _ in range(attempts_count):
                try:
                    return await coroutine(*args, **kwargs)
                except Exception as ex:
                    free_attempts -= 1
                    logger.warning("Parser error: %s" % ex)

                await asyncio.sleep(delay)

            if raise_exc and free_attempts == 0:
                raise ParserExpcetion

        return wrapper

    return decorator
