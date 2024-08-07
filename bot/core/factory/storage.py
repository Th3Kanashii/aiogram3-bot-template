from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.mongo import MongoStorage
from aiogram.fsm.storage.redis import RedisStorage
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import ConnectionPool, Redis


if TYPE_CHECKING:
    from bot.config import Config


def get_storage(config: Config) -> MemoryStorage | RedisStorage | MongoStorage:
    """
    Creates and configures a Telegram bot dispatcher.

    :param config: A configuration object containing necessary settings.
    :return: An instance of the Dispatcher for the Telegram bot.
    """
    # hatch run pip install '.[redis]'
    if config.bot.use_redis:
        redis: Redis = Redis(
            connection_pool=ConnectionPool(
                host=config.redis.host,
                port=config.redis.port,
                db=config.redis.db,
            ),
        )
        return RedisStorage(redis=redis)

    # hatch run pip install '.[mongo]'
    if config.bot.use_mongo:
        client: AsyncIOMotorClient = AsyncIOMotorClient(config.mongo.uri)
        return MongoStorage(client=client)

    return MemoryStorage()
