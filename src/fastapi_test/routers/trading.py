from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from ..cache import get_cached, set_cached

from ..schemas.trading import (
    DynamicsQuery,
    LastDatesQuery,
    SpimexTradingResultRead,
    TradingResultsQuery,
)

from ..repositories.trading import TradingRepository

from ..database import get_session


router = APIRouter(prefix="/api/trading", tags=["Trading"])


@router.get("/last-dates", response_model=list[date])
async def last_dates(
    request: Request,
    query: LastDatesQuery = Query(),
    session: AsyncSession = Depends(get_session),
):
    cached = await get_cached(request)
    if cached:
        return cached

    repo = TradingRepository(session)
    result = await repo.get_last_trading_dates(**query.model_dump())

    cached_data = jsonable_encoder(result)
    await set_cached(request, cached_data)

    return result


@router.get("/dynamics", response_model=list[SpimexTradingResultRead])
async def dynamics(
    request: Request,
    query: DynamicsQuery = Query(),
    session: AsyncSession = Depends(get_session),
):
    cached = await get_cached(request)
    if cached:
        return cached

    repo = TradingRepository(session)
    result = await repo.get_dynamics(**query.model_dump())

    cached_data = jsonable_encoder(result)
    await set_cached(request, cached_data)

    return result


@router.get("/results", response_model=list[SpimexTradingResultRead])
async def results(
    request: Request,
    query: TradingResultsQuery = Query(),
    session: AsyncSession = Depends(get_session),
):
    cached = await get_cached(request)
    if cached:
        return cached

    repo = TradingRepository(session)
    result = await repo.get_trading_results(**query.model_dump())

    cached_data = jsonable_encoder(result)
    await set_cached(request, cached_data)

    return result
