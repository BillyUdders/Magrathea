from sqlalchemy import Boolean, Float, Integer, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column

from magrathea.database import Base


class Map(Base):
    __tablename__ = "maps"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    size: Mapped[int] = mapped_column(Integer)
    octaves: Mapped[int] = mapped_column(Integer)
    seed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    island_density: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_pregenerated: Mapped[bool] = mapped_column(Boolean, default=False)
    data: Mapped[bytes] = mapped_column(LargeBinary)
