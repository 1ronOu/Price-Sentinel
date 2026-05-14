from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_current_user
from app.core.database import get_db
from app.models.user_models import User
from app.schemas.item_schema import ItemOut
from app.schemas.coin_schema import CoinCreate
from app.cruds import item_crud, coin_crud


router = APIRouter(
    prefix='/item',
    tags=['items']
)

@router.post('/create', response_model=ItemOut)
async def create_item(
    coin: CoinCreate,
    target_price: Decimal,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    user_id = user.id
    return await coin_crud.create_coin(coin=coin, db=db, target_price=target_price, user_id=user_id)


@router.get('/get_multiple_items')
async def get_multiple_items(db: AsyncSession = Depends(get_db)):
    items = await item_crud.get_multiple_items(db=db)
    return items

@router.get('/read_all', response_model=list[ItemOut])
async def read_all_items(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user_id = user.id
    return await item_crud.read_items(db=db, user_id=user_id)


@router.delete('/delete_item/{item_id}')
async def delete_item(
        item_id: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user_id = user.id
    await item_crud.delete_item(item_id=item_id, db=db, user_id=user_id)

@router.get('/all_history')
async def get_all_history(db: AsyncSession = Depends(get_db)):
    return await item_crud.get_history(db=db)


@router.put('/update_target_price')
async def update_target_price(
        item_id: int,
        target_price: Decimal,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user_id = user.id
    updated_item = await item_crud.update_target_price(
        item_id=item_id,
        target_price=target_price,
        db=db,
        user_id=user_id
    )
    return updated_item