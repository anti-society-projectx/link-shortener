from httpx import AsyncClient

from telegram_bot.api.exceptions import ObjectAlreadyExistError, ObjectNotFoundError, InvalidUrlError
from telegram_bot.api.schemas.link import ResponseReadLinks, ResponseReadLink, ResponseReadLinkClicks
from telegram_bot.api.schemas.user import ResponseReadUser
from telegram_bot.core.config import settings
from telegram_bot.core.logger import logger


class ApiClient:
    def __init__(self) -> None:
        self._client = AsyncClient(
            # base_url="http://127.0.0.1:8000/api/v1",
            base_url=self._get_base_url(),
            timeout=10.0
        )

    async def aclose(self) -> None:
        await self._client.aclose()
        logger.debug("Соединение HTTP-клиента закрыто.")

    async def create_user(self, tg_id: int) -> ResponseReadUser:
        try:
            resp = await self._client.post("/users/", json={"tg_id": tg_id})
            resp.raise_for_status()

            logger.debug("Пользователь с tg_id %s был успешно создан", tg_id)
            return ResponseReadUser.model_validate(resp.json())
        except:
            raise ObjectAlreadyExistError()

    async def create_link(self, user_id: int, url: str) -> ResponseReadLink:
        try:
            resp = await self._client.post("/links/", json={"user_id": user_id, "url": url})
            resp.raise_for_status()

            return ResponseReadLink.model_validate(resp.json())
        except:
            raise InvalidUrlError()

    async def read_user(self, tg_id: int) -> ResponseReadUser:
        try:
            resp = await self._client.get(f"/users/telegram/{tg_id}")
            resp.raise_for_status()

            return ResponseReadUser.model_validate(resp.json())
        except:
            raise ObjectNotFoundError()

    async def read_user_links(self, user_id: int, page: int = 1, page_size: int = 15) -> ResponseReadLinks:
        params = {
            "page": page,
            "page_size": page_size
        }
        resp = await self._client.get(f"/users/{user_id}/links", params=params)
        return ResponseReadLinks.model_validate(resp.json())

    async def read_link_data(self, link_id: int) -> ResponseReadLink:
        try:
            resp = await self._client.get(f"/links/{link_id}")
            resp.raise_for_status()

            return ResponseReadLink.model_validate(resp.json())
        except:
            raise ObjectNotFoundError()

    async def read_link_clicks(self, link_id: int, page: int = 1, page_size: int = 15) -> ResponseReadLinkClicks:
        params = {
            "page": page,
            "page_size": page_size
        }
        resp = await self._client.get(f"/links/{link_id}/clicks", params=params)

        return ResponseReadLinkClicks.model_validate(resp.json())

    @staticmethod
    def _get_base_url() -> str:
        if settings.fastapi.domain != "localhost":
            url_user = settings.fastapi.url_domain
        else:
            url_user = settings.fastapi.url_ip_address

        return url_user + "/api/v1"
