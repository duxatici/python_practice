from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Date, DateTime, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class SpimexTradingResults(Base):
    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column(String(25))
    exchange_product_name: Mapped[str] = mapped_column()
    oil_id: Mapped[str] = mapped_column(String(4))
    delivery_basis_id: Mapped[str] = mapped_column(String(3))
    delivery_basis_name: Mapped[str] = mapped_column(String(50))
    delivery_type_id: Mapped[str] = mapped_column(String(1))
    volume: Mapped[int] = mapped_column()
    total: Mapped[Decimal] = mapped_column(Numeric(16, 2))
    count: Mapped[int] = mapped_column()
    date: Mapped[date] = mapped_column(Date)
    created_on: Mapped[datetime] = mapped_column(DateTime)
    updated_on: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
