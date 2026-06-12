from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from telegram_bot.api.schemas.link import ResponseReadLink, ResponseReadLinkClick
from telegram_bot.utils.link import get_flag_emoji, reformat_datetime


def start_cmd_kb():
    builder = ReplyKeyboardBuilder()

    builder.add(
        KeyboardButton(text="🔗Сократить ссылку"),
        KeyboardButton(text="📊Мои ссылки")
    )

    return (builder.adjust(1)).as_markup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Меню"
    )


def build_user_links(
        user_links: list[ResponseReadLink],
        page: int,
        pages: int
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    for user_link in user_links:
        builder.button(
            text=f"{user_link.short_code} | {user_link.url}",
            callback_data=f"link-{user_link.id}"
        )

    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f"user-links-page-{page - 1 if page > 1 else 1}",
            icon_custom_emoji_id="5255703720078879038"
        ),
        InlineKeyboardButton(
            text=f"{page}/{pages}",
            callback_data="non-callback"
        ),
        InlineKeyboardButton(
            text='Вперёд',
            callback_data=f"user-links-page-{page + 1 if page < pages else 1}",
            icon_custom_emoji_id="5253767677670862169"
        )
    )

    return builder.as_markup()


def build_link_clicks(
        user_link_clicks: list[ResponseReadLinkClick],
        page: int,
        pages: int
):
    builder = InlineKeyboardBuilder()
    link_id = 0

    for user_link_click in user_link_clicks:
        builder.button(
            text=f"{get_flag_emoji(user_link_click.country_code)} | {reformat_datetime(user_link_click.clicked_at)}",
            callback_data=f"click-{user_link_click.id}"
        )
        link_id = user_link_click.link_id

    builder.adjust(1)

    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=f"user-click-page-{link_id}-{page - 1 if page > 1 else 1}",
            icon_custom_emoji_id="5255703720078879038"
        ),
        InlineKeyboardButton(
            text=f"{page}/{pages}",
            callback_data="non-callback"
        ),
        InlineKeyboardButton(
            text='Вперёд',
            callback_data=f"user-click-page-{link_id}-{page + 1 if page < pages else 1}",
            icon_custom_emoji_id="5253767677670862169"
        )
    )

    return builder.as_markup()
