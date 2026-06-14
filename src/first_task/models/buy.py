from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base
from models.book import Book


class Buy(Base):
    __tablename__ = "buys"

    buy_id: Mapped[int] = mapped_column(primary_key=True)
    buy_description: Mapped[str] = mapped_column(String(255))
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.client_id"))

    books: Mapped[list["Book"]] = relationship(secondary="buy_books")
    steps: Mapped[list["Book"]] = relationship(
        secondary="buy_steps", back_populates="buys"
    )
