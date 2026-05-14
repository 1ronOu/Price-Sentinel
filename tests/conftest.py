import asyncio

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app
from tests.factories.user_factorie import UserFactory

pytest_plugins = [
    'tests.fixtures.db_record_create',
    'tests.fixtures.authorization'
]

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(settings.SQLALCHEMY_TEST_DATABASE_URI)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def db(engine):
    connection = await engine.connect()
    trans = await connection.begin()

    session = AsyncSession(bind=connection, expire_on_commit=False)

    yield session

    await session.close()
    await trans.rollback()
    await connection.close()


@pytest.fixture
async def client(db: AsyncSession):
    async def get_test_db():
        yield db

    app.dependency_overrides[get_db] = get_test_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
async def set_session_for_factories(db: AsyncSession):
    UserFactory._meta.sqlalchemy_session = db


