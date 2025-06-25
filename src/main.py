from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from starlette.middleware.sessions import SessionMiddleware

from src.apis import api_router
from src.auth.dependencies import AdminUserDep, CurrentUserDep
from src.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    # Add Middlewares
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

    # include all routers
    app.include_router(api_router)

    return app


app = create_app()

# Add Metrics
instrumentator = Instrumentator(
    should_group_status_codes=False, excluded_handlers=[".*admin.", "/metrics"]
)
instrumentator.instrument(app).expose(app)


@app.get("/user-test")
async def user_info(current_user: CurrentUserDep):
    return {"username": current_user.username, "email": current_user.email}


@app.get("/admin-test")
async def admin_info(admin_user: AdminUserDep):
    return {
        "username": admin_user.username,
        "email": admin_user.email,
        "role": admin_user.role,
    }
