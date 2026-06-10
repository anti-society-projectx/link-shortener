from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DbConfig(BaseModel):
    """
    Настройки подключения к базе данных.
    """

    hostname: str = Field(
        "postgres",
        description="Имя контейнера для подключения к БД"
    )
    user: str = Field(
        ...,
        description="Имя пользователя для подключения к БД"
    )
    password: str = Field(
        ...,
        description="Пароль для подключения к БД"
    )
    db: str = Field(
        ...,
        description="Имя БД"
    )
    port: int = Field(
        5432,
        description="Порт для подключения к БД"
    )

    @property
    def url(self) -> str:
        """
        Возвращает URL для подключения к БД по имени хоста
        """
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.db}"


class FastapiConfig(BaseModel):
    """
    Конфигурационный класс для запуска FastAPI-приложения.
    """
    hostname: str = "backend"
    ip_address: str = "0.0.0.0"
    domain: str = "localhost"
    port: int = 8000
    prod: bool = False
    https: bool = False
    workers: int = 1


class Setting(BaseSettings):
    """
    Главный конфигурационный класс приложения.
    """
    model_config = SettingsConfigDict(
        env_file=(".env.example", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="allow",
    )
    db: DbConfig
    fastapi: FastapiConfig = FastapiConfig()
