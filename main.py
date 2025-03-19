import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from app.log_handlers import TelegramLogsHandler
from app.router import router as devman_router
from app.settings import settings


class DevmanBot:
    def __init__(self, bot_token: str, admin_id: str, log_format: str, log_level: str):
        self.bot_token = bot_token

        self.admin_id = admin_id
        self.log_format = log_format
        self.log_level = log_level

    async def run(self):
        async with Bot(token=self.bot_token).context() as bot:
            await self._setup_logging(bot)

            await bot.set_my_commands(
                commands=[
                    BotCommand(command='start', description='Запустить бота'),
                ]
            )

            dp = Dispatcher()
            dp.include_router(devman_router)
            await dp.start_polling(bot)

    async def _setup_logging(self, bot: Bot):
        logging.basicConfig(level=self.log_level, format=self.log_format)

        telegram_handler = TelegramLogsHandler(bot=bot, chat_id=self.admin_id)
        telegram_handler.setFormatter(logging.Formatter('%(message)s'))
        telegram_handler.setLevel(logging.WARNING)
        logging.getLogger().addHandler(telegram_handler)


if __name__ == '__main__':
    while True:
        try:
            asyncio.run(
                DevmanBot(
                    bot_token=settings.bot_token,
                    admin_id=settings.admin_id,
                    log_format=settings.log_format,
                    log_level=settings.log_level,
                ).run()
            )
        except Exception as e:
            logging.critical('Бот упал с ошибкой')
            logging.critical(e, exc_info=True)
            asyncio.run(asyncio.sleep(settings.restart_delay))
