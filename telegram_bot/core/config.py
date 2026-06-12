from typing import Literal

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramBotConfig(BaseModel):
    api_token: str = Field(
        ...,
        description="API-токен Telegram Bot'а (tg:@botfather)"
    )


class LoggingConfig(BaseModel):
    """
    Настройки логирования приложения
    """
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"


class FastapiConfig(BaseModel):
    """
    Конфигурационный класс для запуска FastAPI-приложения.
    """
    hostname: str = "backend"
    ip_address: str = "127.0.0.1"
    domain: str = "localhost"
    port: int = 8000
    https: bool = False
    prod: bool = False

    @property
    def url_ip_address(self) -> str:
        """
        Возвращает базовый URL-адрес приложения на основе IP-адреса.
        Пример: http://127.0.0.1:8000 или https://127.0.0.1
        """
        protocol = "https" if self.https else "http"
        is_standard_port = (protocol == "http" and self.port == 80) or (protocol == "https" and self.port == 443)
        port_suffix = "" if is_standard_port else f":{self.port}"
        return f"{protocol}://{self.ip_address}{port_suffix}"

    @property
    def url_domain(self) -> str:
        """Возвращает URL-адрес на основе домена (например, https://localhost)."""
        protocol = "https" if self.https else "http"
        is_standard_port = (protocol == "http" and self.port == 80) or (protocol == "https" and self.port == 443)
        port_suffix = "" if is_standard_port else f":{self.port}"
        return f"{protocol}://{self.domain}{port_suffix}"


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="allow",
    )
    telegram_bot: TelegramBotConfig
    logging: LoggingConfig = LoggingConfig()
    fastapi: FastapiConfig = FastapiConfig()


settings = Setting()
