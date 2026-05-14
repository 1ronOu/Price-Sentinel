import pytest
from aiofiles.os import access
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.jwt_service import create_access_token
from tests.factories.user_factorie import UserFactory


@pytest.fixture(scope="function")
async def client_user(client: AsyncClient, db: AsyncSession):
    user = UserFactory()
    db.add(user)
    await db.flush()
    await db.refresh(user)
    payload = {
        'sub': user.name,
        'user_id': user.id
    }
    access_token = await create_access_token(payload=payload)
    headers = {"Authorization": f"Bearer {access_token}"}
    client.headers.update(headers)
    yield client
    client.headers.clear()