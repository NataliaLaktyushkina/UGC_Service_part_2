import abc
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from datetime import datetime


class AbstractDB(abc.ABC):

    @abc.abstractmethod
    def add_bookmark(self, movie_id: str, user_id: str) -> bool:
        pass


class MongoDB(AbstractDB):
    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.bookmark_db = self.client.bookmark_database

    async def add_bookmark(self, movie_id: str, user_id: str) -> bool:
        """Add bookmark to Mongo DB"""
        # bookmark_collection = self.bookmark_db[user_id]
        bookmark_collection = self.bookmark_db["test_collection"]
        bookmark_was_added = await self.do_insert_bookmark(bookmark_collection,
                                                           movie_id)
        return bookmark_was_added

    async def do_insert_bookmark(self, collection: AsyncIOMotorCollection,
                                 movie_id: str) -> bool:
        document = {"movie_id": movie_id}
        result = await self.bookmark_db["test_collection"].insert_one(document)
        if result.inserted_id:
            return True
        return False
