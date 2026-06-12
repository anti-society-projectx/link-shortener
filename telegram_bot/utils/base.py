import datetime


def get_welcome_text(
        firstname: str
) -> str:
    hours_now = datetime.datetime.now().hour
    text_welcome = {
        "4-12": "🌅Доброе утро",
        "13-17": "☀️Добрый день",
        "18-22": "🌇Добрый вечер",
        "23-4": "🌑Доброй ночи"
    }

    for k, v in text_welcome.items():
        up, to = k.split("-")

        if int(up) <= hours_now <= int(to):
            return f"{v}, {firstname}"
