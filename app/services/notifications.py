from app.core.loader import get_bot
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_models import User


async def send_notifications(items: list, db: AsyncSession):
    bot = get_bot()
    if items:
        for item in items:
            text = (
                f"🔔 **Сигнал по цене!**\n\n"
                f"Монета: # {item.coin.title}\n"
                f"Целевая цена: {item.target_price}\n"
                f"Текущая цена: {item.coin.price}\n"
            )
            await bot.send_message(
                chat_id=item.user.telegram_id,
                text=text,
                parse_mode='Markdown'
            )
            item.is_notified = True
        await db.commit()