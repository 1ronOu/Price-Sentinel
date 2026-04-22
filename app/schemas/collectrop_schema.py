from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CurrentPriceUsd(BaseModel):
    usd: Decimal


class CurrentPrices(BaseModel):
    current_price: CurrentPriceUsd


class DescriptionLanguage(BaseModel):
    en: str


class CoinData(BaseModel):
    id: str
    market_data: CurrentPrices
    description: DescriptionLanguage
    symbol: str
    model_config = ConfigDict(from_attributes=True) 
