from secrets import token_urlsafe
from typing import NewType

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import (
    BaseSettings as _BaseSettings,
    SettingsConfigDict,
)
from sqlalchemy import URL


MONGO_URI = NewType("MONGO_URI", str)
WEBHOOK_URL = NewType("WEBHOOK_URL", str)


class BaseSettings(_BaseSettings):
    """
    Base settings class.
    """

    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")


class BotConfig(BaseSettings, env_prefix="BOT_"):
    """
    Bot settings.

    Attributes:
        token (SecretStr): Bot token.
        use_redis (bool): Use Redis.
        use_mongo (bool): Use Mongo.
        drop_pending_updates (bool): Drop pending updates.
    """

    token: SecretStr
    use_redis: bool
    use_mongo: bool
    drop_pending_updates: bool


class WebhookConfig(BaseSettings, env_prefix="WEBHOOK_"):
    """
    Webhook settings.

    Attributes:
        use (bool): Use webhook.
        reset (bool): Reset webhook.
        base_url (str): Base URL.
        path (str): Path.
        port (int): Port.
        host (str): Host.
        secret_token (SecretStr): Secret token.
    """

    use: bool
    reset: bool
    base_url: str
    path: str
    port: int
    host: str
    secret_token: SecretStr = Field(default_factory=token_urlsafe)

    @property
    def url(self) -> WEBHOOK_URL:
        """
        Build webhook URL.

        :return: Webhook URL.
        """
        return f"{self.base_url}{self.path}"


class PostgresConfig(BaseSettings, env_prefix="POSTGRES_"):
    """
    Postgres settings.

    Attributes:
        host (str): Host.
        db (str): Database name.
        password (SecretStr): Password.
        port (int): Port.
        user (str): User.
        data (str): Data.
    """

    host: str
    db: str
    password: SecretStr
    port: int
    user: str
    data: str

    @property
    def dsn(self) -> URL:
        """
        Build data source name.

        :return: Database URL.
        """
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.db,
        )


class RedisConfig(BaseSettings, env_prefix="REDIS_"):
    """
    Redis settings.

    Attributes:
        host (str): Host.
        port (int): Port.
        db (int): Database number.
        data (str): Data.
    """

    host: str
    port: int
    db: int
    data: str


class MongoConfig(BaseSettings, env_prefix="MONGO_"):
    """
    Mongo settings.

    Attributes:
        host (str): Host.
        port (int): Port.
        db (str): Database name.
        user (str): User.
        password (SecretStr): Password.
    """

    host: str
    port: int
    db: str
    user: str
    password: SecretStr
    data: str

    @property
    def uri(self) -> MONGO_URI:
        """
        Build Mongo URI.

        :return: Mongo URI.
        """
        return f"mongodb://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class Config(BaseModel):
    """
    Configuration settings.

    Attributes:
        bot (BotConfig): Bot settings.
        postgres (PostgresConfig): Postgres settings.
        redis (RedisConfig): Redis settings.
        mongo (MongoConfig): Mongo settings.
    """

    bot: BotConfig
    postgres: PostgresConfig
    webhook: WebhookConfig
    redis: RedisConfig | None = None
    mongo: MongoConfig | None = None


def create_config() -> Config:
    """
    Load configuration settings.

    :return: Configuration settings.
    """
    return Config(
        bot=BotConfig(),
        postgres=PostgresConfig(),
        webhook=WebhookConfig(),
    )
