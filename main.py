import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.router import router as devman_router
from app.settings import settings


async def main():
    logging.basicConfig(level=settings.log_level, format=settings.log_format)

    async with Bot(token=settings.bot_token).context() as bot:
        await bot.set_my_commands(
            commands=[
                BotCommand(command='start', description='Запустить бота'),
            ]
        )

        dp = Dispatcher()
        dp.include_router(devman_router)
        await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
