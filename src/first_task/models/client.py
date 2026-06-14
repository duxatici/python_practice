from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class Client(Base):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True)
    name_client: Mapped[str] = mapped_column(String(255))
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.city_id"))
