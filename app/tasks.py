import asyncio
import logging

from celery import shared_task, Celery
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.crud import  update_item_current_price, read_items, get_multiple_items
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings
from app.core.celery_app import celery_app


logger = logging.getLogger(__name__)

async def run_update_price(item_id: int):
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, expire_on_commit=False) 
    async with session_factory() as db:
        try:
            await update_item_current_price(item_id=item_id, db=db)
        except Exception as e:
            await db.rollback()
            raise
        finally:
            await db.close()
    await engine.dispose()


@shared_task(name='update_item_current_price_task')
def update_item_price(item_id: int):
    logger.info(f'Price update started for item {item_id}')
    try:
        asyncio.run(run_update_price(item_id=item_id))
        logger.info(f'Price for item {item_id} updated successfully')
    except Exception as e:
        logger.error(f'An error occurred during the update')
        raise e
    

async def run_update_multiple_prices():
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    session_factory = async_sessionmaker(engine, expire_on_commit=False) 
    async with session_factory() as db:
        try:
            await get_multiple_items(db=db)
        except Exception as e:
            await db.rollback()
            raise e
        finally:
            await db.close()
    await engine.dispose()


    
@shared_task(name='update_multiple_item_prices')
def update_multiple_item_prices():
    try:
        asyncio.run(run_update_multiple_prices())
    except Exception as e:
        logger.error(f'An error occurred during the update')
        raise e
    