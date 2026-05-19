from typing import Dict

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.parametrize(
    'payload, expected_status_code',
    [
        ({'name': 'foo', 'password': 'bar'}, 200),
        ({'name': 123, 'password': 'bar'}, 422),
    ]
)
async def test_create_user(
        client: AsyncClient,
        db: AsyncSession,
        payload: Dict[str, str],
        expected_status_code: int,
):
    response = await client.post(url='/user/', json=payload)
    if expected_status_code == 200:
        data = response.json()
        assert 'id' in data
        assert data['name'] == payload['name']
        assert 'password' not in data
    assert response.status_code == expected_status_code


async def test_read_user(
        client_user: AsyncClient,
        db: AsyncSession,
):
    response = await client_user.get(url='/user/')

    assert response.status_code == 200
    assert response.json()['name'] == 'admin'


async def test_read_all_users(
        client_user: AsyncClient,
        db: AsyncSession,
):
    response = await client_user.get(url='/user/get_all')

    assert response.status_code == 200
    assert len(response.json()) > 0


async def test_refresh(
        client_user: AsyncClient,
        db: AsyncSession,
):
    response = await client_user.post(url='/user/refresh')

    assert response.status_code == 200
    assert 'access_token' in response.json()