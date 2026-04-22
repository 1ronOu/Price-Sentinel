from fastapi import Depends, FastAPI
from app.core.config import settings
from app.core.database import get_db
from app.routes import items_router
from app.schemas.collectrop_schema import CoinData
from app.services.collector import get_crypto_by_id
from app.tasks import update_item_price
from app.crud import read_item
import os
from app.core.celery_app import celery_app
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

app.include_router(items_router.router)

@app.get('/')
async def health_check():
    return {
        'user': settings.POSTGRES_USER,
        'pass': settings.POSTGRES_PASSWORD,
        'db': settings.POSTGRES_DB,
        'url': settings.SQLALCHEMY_DATABASE_URI,
        'redis': settings.REDIS_URL
        }

@app.get('/get_crypto')
async def test(
    item_id: int,
    ):
    update_item_price.delay(item_id)
