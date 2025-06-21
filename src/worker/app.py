import asyncio 
from asyncio import AbstractEventLoop 
from collections.abc import Callable
from functools import wraps 
from typing import Any, TypeVar

from celery import Celery

from src.config import settings


T = TypeVar("T")


class AsyncCelery(Celery): 
    def __init__(self, *args: Any, **kwargs: Any) -> None: 
        super().__init__(*args, **kwargs) 

        self.functions: dict[str, Callable[..., Any]] = {} 
        self.loop = asyncio.get_event_loop() 

    def task(self, task: Callable[..., T] | None = None, **opts: Any) -> Callable: 
        create_task = super().task 

        def decorator(func: Callable[..., T]) -> Callable[..., T]: 
            @create_task(**opts)
            @wraps(func) 
            def wrapper(*args: Any, loop: AbstractEventLoop | None = None, **kwargs: Any) -> T: 
                loop = loop or self.loop 
                return loop.run_until_complete(func(*args, **kwargs))
            
            self.functions[wrapper.name] = func 
            return wrapper 

        if task: 
            return decorator(task) 
        
        return decorator 


async_celery = AsyncCelery(
    "background_tasks", 
    broker=settings.REDIS_URL
)
async_celery.conf.timezone = "UTC"
async_celery.autodiscover_tasks(packages=["src.worker.tasks"])
async_celery.conf.worker_proc_alive_timeout = 30 
