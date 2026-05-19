from decimal import Decimal
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient
import respx

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item_models import Coin
from tests.helpers.mock_helpers import mock_gecko_for_single_coin, mock_gecko_for_multiple_coins
from tests.helpers.precreate_helper import precreate_item_with_user, precreate_item_with_coin


# --------------------------- item/create ---------------------------
@respx.mock
@pytest.mark.parametrize(
    "payload, target_price, expected_status_code, mock_api_status, should_precreate",
    [
        ({'title': 'bitcoin'}, 50000, 405, 200, True),
    ]
)
async def test_create_item_already_exists(
        db: AsyncSession,
        client_user: AsyncClient,
        payload: dict[str, str],
        target_price: Decimal,
        expected_status_code: int,
        mock_api_status: int,
        should_precreate: bool,
):
    route = mock_gecko_for_single_coin(coin_api_id=payload['title'], status_code=mock_api_status)

    if should_precreate:
        await precreate_item_with_user(db=db)

    response = await client_user.post(
        f'/item/?target_price={target_price}',
        json=payload
    )

    assert route.called
    assert response.status_code == expected_status_code


@respx.mock
@pytest.mark.parametrize(
    "payload, target_price, expected_status_code",
    [
        ({'title': 'bitcoin'}, 50000, 200)
    ]
)
async def test_create_item_success(
        payload: dict[str, str],
        target_price: Decimal,
        expected_status_code: int,
        client_user: AsyncClient,
):
    route = mock_gecko_for_single_coin(coin_api_id=payload['title'], status_code=expected_status_code)

    response = await client_user.post(
        f'/item/?target_price={target_price}',
        json=payload
    )
    assert route.called
    assert response.status_code == expected_status_code


@respx.mock
@pytest.mark.parametrize(
    "payload, target_price, expected_status_code, mock_api_status",
    [
        ({'title': 'bitcoin'}, 'qwe', 422, 200),
        ({'title': 'non_existent_coin'}, 50000, 404, 404),
        ({'title': 'bitcoin'}, 50000, 500, 500),
    ]
)
async def test_create_item_failure(
        payload: dict[str, str],
        target_price: Decimal,
        expected_status_code: int,
        mock_api_status: int,
        client_user: AsyncClient,
):
    route = mock_gecko_for_single_coin(coin_api_id=payload['title'], status_code=mock_api_status)
    response = await client_user.post(
            f'/item/?target_price={target_price}',
        json=payload
    )

    if expected_status_code != 422:
        assert route.called
    else:
        assert not route.called
    assert response.status_code == expected_status_code


# --------------------------- item/read_all ---------------------------
@pytest.mark.parametrize(
    'expected_status_code, should_precreate',
    [
        (200, False),
        (200, True),
    ]
)
async def test_read_all_items(
        client_user: AsyncClient,
        db: AsyncSession,
        expected_status_code: int,
        should_precreate: bool,
):
    if should_precreate:
        await precreate_item_with_user(db=db)

    response = await client_user.get(f'/item/')

    if should_precreate:
        assert response.status_code == expected_status_code
        assert len(response.json()) != 0
    else:
        assert response.status_code == expected_status_code
        assert len(response.json()) == 0


# --------------------------- item/delete_item ---------------------------
@pytest.mark.parametrize(
    'item_id, expected_status_code',
    [
        (None, 200),
        (999, 404),
        ('string', 422)
    ]
)
async def test_delete_item(
        client_user: AsyncClient,
        db: AsyncSession,
        expected_status_code: int,
        item_id: None | int
):
    if item_id is None:
        item = await precreate_item_with_user(db=db)
        item_id = item.id
    response = await client_user.delete(f'/item/{item_id}')
    assert response.status_code == expected_status_code

# --------------------------- item/update_item ---------------------------
@pytest.mark.parametrize(
    'item_id, expected_status_code, payload',
    [
        (None, 200, {'target_price': 1000}),
        (999, 404, {'target_price': 1000}),
        (None, 422, {'target_price': 'qwe'}),
    ]
)
async def test_update_item(
        client_user: AsyncClient,
        db: AsyncSession,
        item_id: None | int ,
        expected_status_code: int,
        payload: dict[str, int | str],
):
    if item_id is None:
        item = await precreate_item_with_user(db=db)
        item_id = item.id
    response = await client_user.put(f'/item/{item_id}', json=payload)
    assert response.status_code == expected_status_code
    assert response.status_code == expected_status_code

# --------------------------- item/get_multiple_prices ---------------------------
@respx.mock
async def test_get_multiple_items(
        client_user: AsyncClient,
        db: AsyncSession,
        coin: Coin,
        monkeypatch
):
    gecko_route = mock_gecko_for_multiple_coins()
    await precreate_item_with_coin(db=db)

    mock_bot = AsyncMock()
    mock_bot.send_message.return_value = AsyncMock()
    import app.services.notifications as notify_module
    monkeypatch.setattr(notify_module, 'get_bot', lambda: mock_bot)

    response = await client_user.get('item/get_multiple_items')

    assert mock_bot.send_message.called
    assert gecko_route.called
    assert response.status_code == 200


