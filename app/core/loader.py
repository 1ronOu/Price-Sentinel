from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp_socks import ProxyConnector
from app.core.config import settings

_bot: Bot = None
_dp: Dispatcher = None


def get_bot() -> Bot:
    global _bot
    if _bot is None:
        connector = ProxyConnector.from_url('socks5://host.docker.internal:7897', rdns=True)
        session = AiohttpSession()
        session.connector = connector
        _bot = Bot(token=settings.TELEGRAM_API, session=session)
    return _bot


def get_dispatcher() -> Dispatcher:
    global _dp
    if _dp is None:
        _dp = Dispatcher()
    return _dp