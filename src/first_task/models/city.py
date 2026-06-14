from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.database import Base
from models.client import Client


class City(Base):
    __tablename__ = "cities"

    city_id: Mapped[int] = mapped_column(primary_key=True)
    name_city: Mapped[str] = mapped_column(String(150), unique=True)
    days_delivery: Mapped[int] = mapped_column()

    clients: Mapped[list["Client"]] = relationship()
