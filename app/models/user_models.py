from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    password: Mapped[bytes]
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=True)
    items = relationship("Item", back_populates='user')
    