from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, HttpUrl


class ItemBase(BaseModel): 
    title: str
    target_price: Decimal
    currencie: str


class ItemCreate(ItemBase):
    pass


class ItemOut(ItemBase):
    id: int
    current_price: Decimal | None = None
    description: str | None = None
    url: HttpUrl | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 

class ItemUpdate(BaseModel):
    title: str | None = None
    target_price: Decimal | None = None
    current_price: Decimal | None = None
    description: str | None = None
    url: HttpUrl | None = None
    created_at: datetime
