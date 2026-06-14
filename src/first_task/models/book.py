from decimal import Decimal

from sqlalchemy import String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.author_id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.genre_id"))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    amount: Mapped[int] = mapped_column()
