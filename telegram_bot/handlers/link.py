from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from telegram_bot.api.client import ApiClient
from telegram_bot.api.exceptions import ObjectNotFoundError, InvalidUrlError
from telegram_bot.core.config import settings
from telegram_bot.keyboards.base import build_user_links, build_link_clicks

router = Router()


class CreateLink(StatesGroup):
    url = State()


@router.message(F.text == "🔗Сократить ссылку")
async def wait_url(message: Message, state: FSMContext):
    await message.answer("Отправь мне текст:")
    await state.set_state(CreateLink.url)


@router.message(CreateLink.url)
async def create_link(message: Message, state: FSMContext, api_client: ApiClient):
    link = message.text

    try:
        user = await api_client.read_user(message.from_user.id)
        await api_client.create_link(user.id, link)

        await message.answer("Ссылка успешно создана.")
    except InvalidUrlError:
        await message.answer("Проверьте правильно ли набрана ссылка?")

    await state.clear()


@router.message(F.text == "📊Мои ссылки")
async def get_user_links(message: Message, api_client: ApiClient):
    user_data = message.from_user
    try:
        user = await api_client.read_user(user_data.id)
        user_links = await api_client.read_user_links(user.id)
        print(user, user_links)

        await message.answer(
            f"🔗Всего ссылок: <code>{user_links.total}</code>",
            reply_markup=build_user_links(
                user_links=user_links.items,
                page=user_links.page,
                pages=user_links.pages
            )
        )

    except ObjectNotFoundError:
        await api_client.create_user(user_data.id)


@router.callback_query(F.data.startswith("link-"))
async def get_link_data(callback: CallbackQuery, api_client: ApiClient):
    # user_data = callback.message.from_user
    link_callback = callback.data.split('-')
    link_id = link_callback[1]
    try:
        link_data = await api_client.read_link_data(link_id)
        link_clicks = await api_client.read_link_clicks(link_id)

        if settings.fastapi.domain != "localhost":
            url_user = settings.fastapi.url_domain + f"/{link_data.short_code}"
        else:
            url_user = settings.fastapi.url_ip_address + f"/{link_data.short_code}"

        await callback.message.answer(
            f"<b>📊Статистика Вашей ссылки:\n\n"
            f"🔗Ваша ссылка: <code>{url_user}</code>\n"
            f"📶Редирект на ресурс: <code>{link_data.url}</code>\n"
            f"🧾Всего переходов по ссылке: <code>{link_clicks.total}</code></b>",
            reply_markup=build_link_clicks(link_clicks.items, link_clicks.page, link_clicks.pages)
        )
    except ObjectNotFoundError:
        await callback.message.answer("Ссылку с таким ID не удалось найти.")

    await callback.answer()


@router.callback_query(F.data.startswith("user-links-page-"))
async def fetch_page(callback: CallbackQuery, api_client: ApiClient):
    user_data = callback.from_user
    link_page = callback.data.split('-')[-1]

    try:
        user = await api_client.read_user(user_data.id)
        user_links = await api_client.read_user_links(user.id, page=link_page)

        await callback.message.edit_reply_markup(
                reply_markup=build_user_links(
                    user_links=user_links.items,
                    page=user_links.page,
                    pages=user_links.pages
                )
        )


    except ObjectNotFoundError:
        await api_client.create_user(user_data.id)
    except TelegramBadRequest:
        pass

    await callback.answer()


@router.callback_query(F.data.startswith("user-click-page-"))
async def fetch_page(callback: CallbackQuery, api_client: ApiClient):
    user_data = callback.from_user
    link_callback_data = callback.data.replace("user-click-page-", "").split('-')
    link_id, link_clicks_page = link_callback_data[0], link_callback_data[1]

    try:
        link_clicks = await api_client.read_link_clicks(link_id, page=link_clicks_page)

        await callback.message.edit_reply_markup(
            reply_markup=build_link_clicks(
                user_link_clicks=link_clicks.items,
                page=link_clicks.page,
                pages=link_clicks.pages
            )
        )

    except ObjectNotFoundError:
        await api_client.create_user(user_data.id)
    except TelegramBadRequest:
        pass

    await callback.answer()
