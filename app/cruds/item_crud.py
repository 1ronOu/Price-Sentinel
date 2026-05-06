from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette import status

from app.schemas.item_schema import ItemCreate
from app.cruds import coin_crud
from app.models.item_models import Item, PriceHistory, Coin
from app.services.collector import get_crypto_by_id, get_multiple_cryptos


async def create_item(
        coin_id: int,
        user_id: int,
        target_price: int,
        db: AsyncSession
):
    new_item = Item(
        user_id=user_id,
        coin_id=coin_id,
        target_price=target_price
    )
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item


async def update_item_current_price(
        item_id: int,
        db: AsyncSession
):
    item = await read_item(item_id=item_id, db=db)
    item_info = await get_crypto_by_id(item.title.lower())
    item.current_price = item_info.market_data.current_price.usd
    await db.commit()


async def get_multiple_items(db: AsyncSession):
    coin_api_ids = await coin_crud.get_coin_api_ids(db=db)
    item_info = await get_multiple_cryptos(coin_ids=coin_api_ids, currency='usd')
    return await coin_crud.update_multiple_items(coin_api_ids=coin_api_ids, items=item_info, db=db)


async def get_history(db: AsyncSession):
    result = await db.execute(select(PriceHistory))
    return result.scalars().all()


async def read_item(
        item_id: int,
        user_id: int,
        db: AsyncSession
):
    query = select(Item).where(Item.id == item_id, Item.user_id == user_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f'Item {item_id} not found'
        )
    return item


async def read_items(
        db: AsyncSession,
        user_id: int
):
    result = await db.execute(select(Item).where(Item.user_id == user_id))
    return result.scalars().all()


async def delete_item(
        db: AsyncSession,
        item_id: int,
        user_id: int
):
    item = await read_item(item_id=item_id, db=db)
    if item.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Access Denied'
        )
    await db.delete(item)
    await db.commit()


async def update_target_price(
        item_id: int,
        user_id: int,
        target_price: Decimal,
        db: AsyncSession
):
    item = await read_item(item_id=item_id, db=db, user=user_id)
    item.target_price = target_price
    item.is_notified = False
    await db.commit()
    return item