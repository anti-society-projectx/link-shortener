from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from telegram_bot.api.client import ApiClient
from telegram_bot.api.exceptions import ObjectNotFoundError, ObjectAlreadyExistError
from telegram_bot.keyboards.base import start_cmd_kb, build_user_links
from telegram_bot.utils.base import get_welcome_text

router = Router()


@router.message(CommandStart())
async def start_cmd(message: Message, api_client: ApiClient):
    user_data = message.from_user
    try:
        await api_client.create_user(user_data.id)
    except ObjectAlreadyExistError:
        pass

    await message.answer(
        f'<b>{get_welcome_text(user_data.first_name)}\n\n'
        f'<tg-emoji emoji-id="5294334197832362643">💻</tg-emoji>'
        f'<a href="https://github.com/anti-society-projectx/link-shortener">Repo</a> | '
        f'<tg-emoji emoji-id="5251447471913057341">👤</tg-emoji>'
        f'<a href="https://zelenka.guru/members/8159799/">Lolz</a></b>',
        reply_markup=start_cmd_kb()
    )
