import abc
from motor.motor_asyncio import AsyncIOMotorClient


class AbstractDB(abc.ABC):

    @abc.abstractmethod
    def add_bookmark(self, movie_id: str, user_id: str) -> bool:
        pass


class MongoDB(AbstractDB):
    def __init__(self, client:AsyncIOMotorClient):
        self.client = client
        self.bookmark_db = self.client.bookmark_database


    async def add_bookmark(self, movie_id: str, user_id: str) -> bool:
        """Add bookmark to Mongo DB"""
        collection = self.bookmark_db.test_collection
        bookmark_was_added = False
        return bookmark_was_added
