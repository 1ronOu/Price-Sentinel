from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Text, false, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.user_models import User #!

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    coin_id: Mapped[int] = mapped_column(ForeignKey('coins.id'))

    target_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[str] = mapped_column(server_default='usd')

    is_notified: Mapped[bool] = mapped_column(server_default=false(), default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user = relationship("User", back_populates='items')
    coin = relationship("Coin", back_populates='items')


class PriceHistory(Base):
    __tablename__ = 'prices'

    id: Mapped[int] = mapped_column(primary_key=True)

    coin_id: Mapped[int] = mapped_column(ForeignKey('coins.id'))

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Coin(Base):
    __tablename__ = 'coins'

    id: Mapped[int] = mapped_column(primary_key=True)

    api_id: Mapped[str] = mapped_column(unique=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str] = mapped_column(String(1024), unique=True, nullable=True)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    items = relationship("Item", back_populates='coin')

