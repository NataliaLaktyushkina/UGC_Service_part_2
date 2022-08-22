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
        self.ugc_db = self.client.ugc_database

    async def add_bookmark(self, movie_id: str, user_id: str) -> bool:
        """Add bookmark to Mongo DB"""
        # bookmark_collection = self.bookmark_db[user_id]
        bookmark_was_added = await self.do_insert_bookmark(user_id,
                                                           movie_id)
        return bookmark_was_added

    async def do_insert_bookmark(self, user_id: str,
                                 movie_id: str) -> bool:
        # document = {
        #     "movie_id": movie_id}
        # first find
        doc = await self.ugc_db["bookmarks"].find_one({"user_id": user_id})
        if doc is None:
            result = await self.ugc_db["bookmarks"].insert_one(
                {"user_id": user_id},
                {"movie_id": movie_id})

            if result.inserted_id:
                return True
        else:
            doc_id = doc["_id"]
            result = await self.ugc_db["bookmarks"].update_one(
                {"_id": doc_id},
                {"$push":
                    {"movie_id": movie_id}
                })

            if result.upserted_id:
                return True

        return False
