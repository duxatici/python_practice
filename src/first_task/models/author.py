from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)
    name_author: Mapped[str] = mapped_column(String(255))
