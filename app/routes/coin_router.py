from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.cruds import coin_crud
from app.schemas.coin_schema import CoinOut

router = APIRouter(
    prefix='/coin',
    tags=['coin']
)


@router.get('/all', response_model=List[CoinOut])
async def get_all_coins(
        db: AsyncSession = Depends(get_db)
):
    return await coin_crud.get_all_coins(db=db)


@router.delete('/delete')
async def delete_coin(coin_id: str ,db: AsyncSession = Depends(get_db)):
    await coin_crud.delete_coin(coin_id=coin_id, db=db)
