from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class Genre(Base):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True)
    name_genre: Mapped[str] = mapped_column(String(50), unique=True)
