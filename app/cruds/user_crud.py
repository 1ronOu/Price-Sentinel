from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.schemas.user_schema import UserCreate, UserOut
from app.models.user_models import User


async def create_user(
        user: UserCreate,
        db: AsyncSession
):
    user_data = user.model_dump()
    new_user = User(**user_data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_user_name(
        user_name: str,
        db: AsyncSession
):
    query = select(User).where(User.name == user_name)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    return user


async def get_user(
        user_id: int,
        db: AsyncSession
):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    return user



async def get_all_users(
        db: AsyncSession
):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


async def update_user(
        chat_id: int,
        user: UserOut,
        db: AsyncSession
):
    user.telegram_id = chat_id
    await db.commit()