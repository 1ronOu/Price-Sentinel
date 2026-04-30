import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.loader import get_bot, get_dispatcher
from app.handlers import commands, registration
from app.middlewares.db import DbSessionMiddleware
from app.models.user_models import User
from app.models.item_models import Item




async def main():
    engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URI, echo=True)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = get_bot()
    dp = get_dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    dp.include_router(commands.router)
    dp.include_router(registration.router)
    
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
