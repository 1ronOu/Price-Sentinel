from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CoinBase(BaseModel): 
    title: str

class CoinCreate(CoinBase):
    pass


class CoinOut(CoinBase):
    id: int
    description: str | None = None
    url: str | None = None
    price: Decimal
    api_id: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 
