import asyncio
import logging

from aiogram import Bot


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot: Bot, chat_id: str):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        message = self.format(record)
        asyncio.create_task(self.bot.send_message(self.chat_id, message))
