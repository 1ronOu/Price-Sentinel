import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories.coin_factory import CoinFactory
from tests.factories.item_factorie import ItemFactory
from tests.factories.user_factorie import UserFactory


@pytest.fixture(scope="function")
async def user(db: AsyncSession):
    user = UserFactory()
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


@pytest.fixture(scope="function")
async def item(db: AsyncSession):
    item = ItemFactory()
    db.add(item)
    await db.flush()
    await db.refresh(item)
    return item


@pytest.fixture(scope="function")
async def coin(db: AsyncSession):
    coin = CoinFactory()
    db.add(coin)
    await db.flush()
    await db.refresh(coin)
    return coin
