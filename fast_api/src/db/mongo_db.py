from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient

mongo_db: Optional[AsyncIOMotorClient] = None


async def get_mongo() -> AsyncIOMotorClient:
    return mongo_db
