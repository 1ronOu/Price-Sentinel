from fastapi import FastAPI
from app.core.config import settings
from app.routes import items_router, user_router, coin_router, login_router

app = FastAPI()

app.include_router(items_router.router)
app.include_router(user_router.router)
app.include_router(coin_router.router)
app.include_router(login_router.router)


@app.get('/')
async def health_check():
    return {
        'user': settings.POSTGRES_USER,
        'pass': settings.POSTGRES_PASSWORD,
        'db': settings.POSTGRES_DB,
        'url': settings.SQLALCHEMY_DATABASE_URI,
        'redis': settings.REDIS_URL
        }