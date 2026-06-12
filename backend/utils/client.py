import geoip2.database
from user_agents import parse

reader = geoip2.database.Reader(
    r"data/GeoLite2-City.mmdb"
)


def parse_ip_address_info(
        ip_address: str
) -> dict[str, str | None]:
    response = reader.city(ip_address)

    return {
        "country_code": response.country.iso_code,
        "city": response.city.name
    }


def parse_user_agent(user_agent: str) -> dict[str, str | None]:
    ua = parse(user_agent or "")

    return {
        "browser": ua.browser.family,
        "os": ua.os.family,
        "device_type": (
            "mobile"
            if ua.is_mobile
            else "tablet"
            if ua.is_tablet
            else "desktop"
            if ua.is_pc
            else "bot"
            if ua.is_bot
            else "unknown"
        ),
    }
