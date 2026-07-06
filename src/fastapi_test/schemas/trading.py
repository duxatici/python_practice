from decimal import Decimal
from datetime import date, datetime, timedelta
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SpimexTradingResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    exchange_product_id: str
    exchange_product_name: str
    oil_id: str
    delivery_basis_id: str
    delivery_basis_name: str
    delivery_type_id: str
    volume: int
    total: Decimal
    count: int
    date: date
    created_on: datetime
    updated_on: Optional[datetime] = None


class LastDatesQuery(BaseModel):
    days: int = Field(3, gt=0)


class TradingResultsQuery(BaseModel):
    oil_id: Optional[str] = None
    delivery_type_id: Optional[str] = None
    delivery_basis_id: Optional[str] = None


class DynamicsQuery(TradingResultsQuery):
    start_date: date = Field(default_factory=lambda: date.today() - timedelta(3))
    end_date: date = Field(default_factory=lambda: date.today())
