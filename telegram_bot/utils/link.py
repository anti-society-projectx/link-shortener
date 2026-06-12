import datetime


def get_flag_emoji(country_code: str | None) -> str:
    if country_code:
        code = country_code.upper()
        if len(code) != 2 or not code.isalpha():
            return "❓"
        return "".join(chr(ord(char) + 127397) for char in code)
    else:
        return "❓"


def reformat_datetime(clicked_at: datetime.datetime) -> str:
    target_tz = datetime.timezone(datetime.timedelta(hours=3))
    local_time = clicked_at.astimezone(target_tz)

    return local_time.strftime("%d.%m.%Y %H:%M")
