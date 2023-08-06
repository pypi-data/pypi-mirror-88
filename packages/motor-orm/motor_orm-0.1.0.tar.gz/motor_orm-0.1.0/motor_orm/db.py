import logging

import motor.motor_asyncio  # type: ignore

from motor_orm.utils import get_subclasses

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, client):
        self.client = client


async def get_db(
    mongodb_database_name: str,
    mongodb_connectionstring: str = "mongodb://127.0.0.1:27017",
    dropdb=False,
) -> Database:
    # Async because on this moment we need to have event loop exists
    client = motor.motor_asyncio.AsyncIOMotorClient(
        mongodb_connectionstring, retryWrites=False
    )

    if dropdb:
        if mongodb_database_name in await client.list_database_names():
            logger.debug(f"Dropping database '{mongodb_database_name}'")
            await client.drop_database(mongodb_database_name)

    dbclient = client[mongodb_database_name]
    db = Database(dbclient)

    from motor_orm.model_service import ModelService

    for model_service_klass in get_subclasses(ModelService):
        model_service = model_service_klass(db)
        await model_service.create_collection()

    return db
