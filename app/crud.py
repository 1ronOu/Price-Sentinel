from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.schemas.items import ItemCreate
from app.models.item_models import Item
from app.services.collector import get_crypto_by_id, get_multiple_cryptos



async def create_item(
        item: ItemCreate,
        db: AsyncSession
):
    item_data = item.model_dump()
    item_info = await get_crypto_by_id(item.title.lower())
    item_data['current_price'] = item_info.market_data.current_price.usd
    item_data['description'] = item_info.description.en
    tv_url = f'https://www.tradingview.com/symbols/{item_info.symbol.upper()}'
    item_data['url'] = tv_url
    new_item = Item(**item_data)

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
    items = await read_items(db=db)
    item_ids = []
    for item in items:
        item_ids.append(item.title)
        currencie = item.currencie
    item_info = await get_multiple_cryptos(coin_ids=item_ids, currencie=currencie)
    return await update_multiple_items(items=item_info, db=db)


async def update_multiple_items(items: dict, db: AsyncSession):
    coin_titles = list(items.keys())
    query = select(Item).where(Item.title.in_(coin_titles))
    result = await db.execute(query)
    
    db_items = result.scalars().all()
    
    items_map = {item.title: item for item in db_items}
    print(items_map)

    for coin_id, currencies_data in items.items():
        item = items_map.get(coin_id)
        if item:
            new_price = next(iter(currencies_data.values()))
            item.current_price = new_price

    await db.commit()


async def read_item(
        item_id: int,
        db: AsyncSession
):
    query = select(Item).where(Item.id == item_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f'Item {item_id} not found'
        )
    return item


async def read_items(
        db: AsyncSession
):
    result = await db.execute(select(Item))
    return result.scalars().all()


async def delete_item(
        db: AsyncSession,
        item_id: int
):
    item = await read_item(item_id=item_id, db=db)
    await db.delete(item)
    await db.commit()