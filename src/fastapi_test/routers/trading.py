from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

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
    query: LastDatesQuery = Query(), session: AsyncSession = Depends(get_session)
):
    repo = TradingRepository(session)
    return await repo.get_last_trading_dates(**query.model_dump())


@router.get("/dynamics", response_model=list[SpimexTradingResultRead])
async def dynamics(
    query: DynamicsQuery = Query(), session: AsyncSession = Depends(get_session)
):
    repo = TradingRepository(session)
    return await repo.get_dynamics(**query.model_dump())


@router.get("/results", response_model=list[SpimexTradingResultRead])
async def results(
    query: TradingResultsQuery = Query(), session: AsyncSession = Depends(get_session)
):
    repo = TradingRepository(session)
    return await repo.get_trading_results(**query.model_dump())
