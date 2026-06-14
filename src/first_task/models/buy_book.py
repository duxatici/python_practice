from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class BuyBook(Base):
    __tablename__ = "buy_books"

    buy_book_id: Mapped[int] = mapped_column(primary_key=True)
    buy_id: Mapped[int] = mapped_column(ForeignKey("buys.buy_id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.book_id"))
    amount: Mapped[int] = mapped_column(default=1)
