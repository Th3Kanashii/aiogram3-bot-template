from bot.core.config import BotConfig, Config, PostgresConfig, WebhookConfig


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
