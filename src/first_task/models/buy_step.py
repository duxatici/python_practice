from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class BuyStep(Base):
    __tablename__ = "buy_steps"

    buy_step_id: Mapped[int] = mapped_column(primary_key=True)
    buy_id: Mapped[int] = mapped_column(ForeignKey("buys.buy_id"))
    step_id: Mapped[int] = mapped_column(ForeignKey("steps.step_id"))
    date_step_beg: Mapped[datetime] = mapped_column(DateTime)
    date_step_end: Mapped[datetime] = mapped_column(DateTime)
