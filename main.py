import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from amocrm.v2 import tokens

from config import BOT_TOKEN, CLIENT_ID, CLIENT_SECRET, SUBDOMAIN, REDIRECT_URL
from handlers import router
from set_bot_commands import set_default_commands


async def main():
    tokens.default_token_manager(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        subdomain=SUBDOMAIN,
        redirect_url=REDIRECT_URL,
        storage=tokens.FileTokensStorage(),
    )

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await set_default_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

