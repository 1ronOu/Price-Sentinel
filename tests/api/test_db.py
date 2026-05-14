from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


async def test_db_connection(db: AsyncSession):
    result = await db.execute(text("SELECT 1"))
    assert result.scalar() == 1