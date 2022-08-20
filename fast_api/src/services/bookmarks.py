from fastapi import Depends
from services.service import AbstractDB, MongoDB
from models.bookmarks import  BookmarkAdded
from db.mongo_db import get_mongo


class BookmarkHandler:
    def __init__(self, bookmark_db: AbstractDB):
        self.bookmark_db = bookmark_db

    async def add_bookmark(self, movie_id: str, user_id: str) -> BookmarkAdded:
        bookmark_added = await self.bookmark_db.add_bookmark(movie_id, user_id)
        return BookmarkAdded(accepted=bookmark_added)


def get_db(
        bookmark_db: AbstractDB = Depends(get_mongo)
) -> BookmarkHandler:
    return BookmarkHandler(MongoDB(bookmark_db))
