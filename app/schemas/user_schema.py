from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, HttpUrl


class UserBase(BaseModel): 
    name: str
    password: str
    telegram_id: int | None = None


class UserCreate(UserBase):
    pass


class UserOut(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True) 

