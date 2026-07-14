from datetime import date
from typing import Sequence

from sqlalchemy import distinct, select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_test.models.spimex_trading_results import SpimexTradingResults


class TradingRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_last_trading_dates(self, days: int = 3) -> Sequence[date]:
        stmt = select(distinct(SpimexTradingResults.date))
        stmt = stmt.order_by(SpimexTradingResults.date.desc())
        stmt = stmt.limit(days)

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_dynamics(
        self,
        oil_id: str | None = None,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Sequence[SpimexTradingResults]:
        stmt = select(SpimexTradingResults)
        if oil_id:
            stmt = stmt.where(SpimexTradingResults.oil_id == oil_id)
        if delivery_type_id:
            stmt = stmt.where(SpimexTradingResults.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            stmt = stmt.where(
                SpimexTradingResults.delivery_basis_id == delivery_basis_id
            )
        if start_date:
            stmt = stmt.where(SpimexTradingResults.date >= start_date)
        if end_date:
            stmt = stmt.where(SpimexTradingResults.date <= end_date)

        stmt = stmt.order_by(SpimexTradingResults.date.desc())

        result = await self.session.execute(stmt)

        return result.scalars().all()

    async def get_trading_results(
        self,
        oil_id: str | None = None,
        delivery_type_id: str | None = None,
        delivery_basis_id: str | None = None,
    ) -> Sequence[SpimexTradingResults]:
        stmt = select(SpimexTradingResults)
        if oil_id:
            stmt = stmt.where(SpimexTradingResults.oil_id == oil_id)
        if delivery_type_id:
            stmt = stmt.where(SpimexTradingResults.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            stmt = stmt.where(
                SpimexTradingResults.delivery_basis_id == delivery_basis_id
            )

        stmt = stmt.limit(100)
        stmt = stmt.order_by(SpimexTradingResults.date.desc())

        result = await self.session.execute(stmt)

        return result.scalars().all()
