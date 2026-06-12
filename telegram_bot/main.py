import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from telegram_bot.api.client import ApiClient
from telegram_bot.core.config import settings
from telegram_bot.core.logger import logger
from telegram_bot.handlers import routers


async def main() -> None:
    api_client = ApiClient()

    bot = Bot(
        settings.telegram_bot.api_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(routers)

    @dp.startup()
    async def startup() -> None:
        logger.info("Бот запущен. Службы успешно запущены.")

    @dp.shutdown()
    async def on_shutdown() -> None:
        await api_client.aclose()
        logger.info("Бот остановлен. Службы остановлены.")

    await dp.start_polling(bot, api_client=api_client)


if __name__ == "__main__":
    asyncio.run(main())
