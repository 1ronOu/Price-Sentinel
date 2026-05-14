from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel): 
    target_price: Decimal
    currency: str = 'usd'
    coin_id: int
    user_id: int
    is_notified: bool


class ItemCreate(ItemBase):
    pass


class ItemOut(ItemBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 

class ItemUpdate(BaseModel):
    target_price: Decimal | None = None

