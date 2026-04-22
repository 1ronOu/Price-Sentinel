from typing import List

from fastapi import HTTPException
import httpx
from app.core.config import settings
from pydantic import ValidationError

from app.schemas.collectrop_schema import CoinData

headers = {'x-cg-pro-api-key': settings.API_KEY}
async def get_crypto_by_id(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}'
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail='Bad request')
        json_data = response.json()
    except httpx.HTTPError:
        raise HTTPException(status_code=500, detail='Error with external api')
    try:
        return CoinData(**json_data)
    except ValidationError:
        raise HTTPException(status_code=502, detail='Invalid data format form provided')
    

async def get_multiple_cryptos(coin_ids: List[str], currencie: str):    
    url = f'https://api.coingecko.com/api/v3/simple/price?vs_currencies={currencie}&ids={','.join(coin_ids)}'
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, headers=headers)
    except httpx.HTTPError:
        raise HTTPException(status_code=500, detail='Error with external api')
    json_data = response.json()
    return json_data
