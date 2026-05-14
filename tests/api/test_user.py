from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.utils import get_current_user_payload
from app.models.item_models import Item, Coin
from app.models.user_models import User


def test_create_user():
    assert True


async def test_get_all_users(db: AsyncSession, user: User):
    assert user.id is not None
    assert user.name is not None


async def test_access_token(client_user:AsyncClient, db: AsyncSession):
    access_token = (client_user.headers.get('Authorization')).split('Bearer ')[1]
    assert access_token is not None
    payload = await get_current_user_payload(token=access_token)
    assert payload['sub'] is not None


async def test_create_item(item: Item):
    assert item.id is not None
    assert item.user_id is not None
    assert item.coin_id is not None


async def test_create_coin(coin: Coin):
    assert coin.id is not None
    assert coin.price is not None