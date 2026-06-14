from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base
from models.buy import Buy


class Step(Base):
    __tablename__ = "steps"

    step_id: Mapped[int] = mapped_column(primary_key=True)
    name_step: Mapped[str] = mapped_column(String(50))

    buys: Mapped[list["Buy"]] = relationship(
        secondary="buy_steps", back_populates="steps"
    )
