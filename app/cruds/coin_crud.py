from decimal import Decimal

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import insert, select
from sqlalchemy.orm import joinedload

from app.models.user_models import User
from app.schemas.coin_schema import CoinCreate
from app.models.item_models import Coin, Item, PriceHistory
from app.services.collector import get_crypto_by_id
from app.services.notifications import send_notifications
from app.cruds import item_crud


async def create_coin(
        coin: CoinCreate,
        target_price: int,
        user_id: int,
        db: AsyncSession
):
    coin_info = await get_crypto_by_id(coin.title.lower())
    coin_exists = await read_coin_by_title(coin_id=coin_info.id, db=db)
    if not coin_exists:
        coin_data = {}
        coin_data['title'] = coin_info.name
        coin_data['price'] = coin_info.market_data.current_price.usd
        coin_data['description'] = coin_info.description.en
        coin_data['api_id'] = coin_info.id
        tv_url = f'https://www.tradingview.com/symbols/{coin_info.symbol.upper()}'
        coin_data['url'] = tv_url
        new_coin = Coin(**coin_data)

        db.add(new_coin)
        await db.flush()
        return await item_crud.create_item(coin_id=new_coin.id, user_id=user_id, target_price=target_price, db=db)
    else:
        return await item_crud.create_item(coin_id=coin_exists.id, user_id=user_id, target_price=target_price, db=db)


async def read_coin_by_title(
        coin_id: str,
        db: AsyncSession
):
    query = select(Coin).where(Coin.api_id == coin_id)
    result = await db.execute(query)
    coin = result.scalar_one_or_none()
    return coin


async def get_coin_api_ids(
        db: AsyncSession
):
    query = select(Coin.api_id).join(Item).distinct()
    result = await db.execute(query)
    db_coins = result.scalars().all()
    coin_api_ids = list(db_coins)
    return coin_api_ids


async def get_all_coins(
        db: AsyncSession
):
    result = await db.execute(select(Coin))
    coins = result.scalars().all()
    return coins


async def compare_prices(coin_prices: dict, db: AsyncSession):
    coin_ids = list(coin_prices.keys())
    query = select(Item).options(joinedload(Item.user),joinedload(Item.coin)).where(Item.coin_id.in_(coin_ids), Item.is_notified == False)
    result = await db.execute(query)
    items = result.scalars().all()

    items_to_notify = []
    for item in items:
        if item.target_price <= coin_prices.get(item.coin_id):
            items_to_notify.append(item)

    return items_to_notify


async def update_multiple_items(coin_api_ids: list, items: dict, db: AsyncSession):
    query = select(Coin).where(Coin.api_id.in_(coin_api_ids))
    result = await db.execute(query)
    
    db_coins = result.scalars().all()
    history = []
    coins_map = {coin.api_id: coin for coin in db_coins}
    coin_prices = {}
    for coin_id, currency_data in items.items():
        coin = coins_map.get(coin_id)
        new_price = next(iter(currency_data.values()))
        coin.price = new_price
        coin_prices[coin.id] = new_price
        history_record = {
            'price': new_price,
            'coin_id': coin.id,
        }
        history.append(history_record)

    if history:
        await db.execute(insert(PriceHistory), history)

        
    await db.commit()

    items_to_notify = await compare_prices(coin_prices=coin_prices, db=db)

    await send_notifications(items=items_to_notify, db=db)


async def delete_coin(db: AsyncSession, coin_id: str):
    coin = await read_coin_by_title(coin_id=coin_id, db=db)
    await db.delete(coin)
    await db.commit()


