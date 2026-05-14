from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item_models import Coin
from app.models.user_models import User
from tests.factories.item_factorie import ItemFactory


async def precreate_item_with_user(
    db: AsyncSession,
):
    users_in_db = await db.execute(select(User))
    user = users_in_db.scalars().first()
    item = ItemFactory(user=user)
    db.add(item)
    await db.flush()
    return item


async def precreate_item_with_coin(
        db: AsyncSession,
):
    coins_in_db = await db.execute(select(Coin))
    coin = coins_in_db.scalars().first()
    users_in_db = await db.execute(select(User))
    user = users_in_db.scalars().first()
    item = ItemFactory(coin=coin, user=user)
    db.add(item)
    await db.flush()
    return item
