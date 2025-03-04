from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.service import get_devman_reviews
from app.settings import settings

router = Router()


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(f'Привет, {message.from_user.first_name}. Бот запущен')

    async for reviews in get_devman_reviews(devman_token=settings.devman_token):
        for review in reviews:
            await message.answer(review, parse_mode='Markdown')
