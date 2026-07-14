import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from redis import asyncio as aioredis

from fastapi_test.exception import (
    BadRequest,
    Forbidden,
    NotFound,
    ServerError,
    Unauthorized,
    UnprocessableEntity,
)

from fastapi_test.config import settings

from fastapi_test.database import engine
from fastapi_test.routers.trading import router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    app.state.redis = redis_client

    yield

    await redis_client.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.exception_handler(NotFound)
async def global_not_found(request: Request, exc: NotFound) -> JSONResponse:
    logger.warning(f"Not found: {exc}")
    return JSONResponse(status_code=404, content={"detail": "Not found"})


@app.exception_handler(BadRequest)
async def global_bad_request(request: Request, exc: BadRequest) -> JSONResponse:
    logger.warning(f"Bad request: {exc}")
    return JSONResponse(status_code=400, content={"detail": "Bad request"})


@app.exception_handler(UnprocessableEntity)
async def global_unprocessable_entity(
    request: Request, exc: UnprocessableEntity
) -> JSONResponse:
    logger.warning(f"Unprocessable entity: {exc}")
    return JSONResponse(status_code=422, content={"detail": "Unprocessable entity"})


@app.exception_handler(Unauthorized)
async def global_unauthorized(request: Request, exc: Unauthorized) -> JSONResponse:
    logger.warning(f"Unauthorized: {exc}")
    return JSONResponse(status_code=401, content={"detail": "Unauthorized"})


@app.exception_handler(Forbidden)
async def global_forbidden(request: Request, exc: Forbidden) -> JSONResponse:
    logger.warning(f"Forbidden: {exc}")
    return JSONResponse(status_code=403, content={"detail": "Forbidden"})


@app.exception_handler(HTTPException)
async def global_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(ServerError)
async def global_server_error(request: Request, exc: ServerError) -> JSONResponse:
    logger.error(f"Server error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
