from datetime import date, datetime, timedelta
from typing import Sequence

from fastapi import APIRouter, Depends, Query, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_test.cache import Cache, get_cache

from fastapi_test.schemas.trading import (
    DynamicsQuery,
    LastDatesQuery,
    SpimexTradingResultRead,
    TradingResultsQuery,
)

from fastapi_test.repositories.trading import TradingRepository

from fastapi_test.database import get_session


router = APIRouter(prefix="/v1/api/trading")


def _ttl_until_1411() -> int:
    now = datetime.now()
    target = now.replace(hour=14, minute=11, second=0, microsecond=0)

    if now >= target:
        target += timedelta(days=1)

    return int((target - now).total_seconds())


def _build_cache_key(request: Request) -> str:
    query = sorted(request.query_params.items())
    query_str = "&".join(f"{k}={v}" for k, v in query)

    return f"{request.method}:{request.url.path}:{query_str}"


def get_repo(session: AsyncSession = Depends(get_session)) -> TradingRepository:
    return TradingRepository(session)


@router.get("/last-dates")
async def last_dates(
    request: Request,
    query: LastDatesQuery = Query(),
    repo: TradingRepository = Depends(get_repo),
    cache: Cache = Depends(get_cache),
) -> Sequence[date]:
    key = _build_cache_key(request)
    cached = await cache.get(key)
    if cached:
        return [date.fromisoformat(item) for item in cached]

    result = await repo.get_last_trading_dates(days=query.days)

    cached_data = jsonable_encoder(result)
    ttl = _ttl_until_1411()
    await cache.set(key, cached_data, ttl)

    return result


@router.get("/dynamics")
async def dynamics(
    request: Request,
    query: DynamicsQuery = Query(),
    repo: TradingRepository = Depends(get_repo),
    cache: Cache = Depends(get_cache),
) -> Sequence[SpimexTradingResultRead]:
    key = _build_cache_key(request)
    cached = await cache.get(key)
    if cached:
        return [SpimexTradingResultRead.model_validate(item) for item in cached]

    result = await repo.get_dynamics(
        oil_id=query.oil_id,
        delivery_type_id=query.delivery_type_id,
        delivery_basis_id=query.delivery_basis_id,
        start_date=query.start_date,
        end_date=query.end_date,
    )

    cached_data = jsonable_encoder(result)
    ttl = _ttl_until_1411()
    await cache.set(key, cached_data, ttl)

    return [SpimexTradingResultRead.model_validate(item) for item in result]


@router.get("/results")
async def results(
    request: Request,
    query: TradingResultsQuery = Query(),
    repo: TradingRepository = Depends(get_repo),
    cache: Cache = Depends(get_cache),
) -> Sequence[SpimexTradingResultRead]:
    key = _build_cache_key(request)
    cached = await cache.get(key)
    if cached:
        return [SpimexTradingResultRead.model_validate(item) for item in cached]

    result = await repo.get_trading_results(
        oil_id=query.oil_id,
        delivery_type_id=query.delivery_type_id,
        delivery_basis_id=query.delivery_basis_id,
    )

    cached_data = jsonable_encoder(result)
    ttl = _ttl_until_1411()
    await cache.set(key, cached_data, ttl)

    return [SpimexTradingResultRead.model_validate(item) for item in result]
