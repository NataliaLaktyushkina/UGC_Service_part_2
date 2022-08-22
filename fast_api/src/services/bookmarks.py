from fastapi import Depends
from services.service import AbstractDB, MongoDB
from models.bookmarks import BookmarkAdded, BookmarksList, BookmarkDeleted
from db.mongo_db import get_mongo


class BookmarkHandler:
    def __init__(self, bookmark_db: AbstractDB):
        self.bookmark_db = bookmark_db

    async def add_bookmark(self, movie_id: str, user_id: str) -> BookmarkAdded:
        bookmark_added = await self.bookmark_db.add_bookmark(movie_id, user_id)
        return BookmarkAdded(added=bookmark_added)

    async def get_bookmarks(self, user_id: str) -> BookmarksList:
        return await self.bookmark_db.get_bookmarks_list(user_id)

    async def delete_bookmark(self, movie_id: str, user_id: str) -> BookmarkDeleted:
        bookmark_deleted = await self.bookmark_db.delete_bookmark(movie_id, user_id)
        return BookmarkDeleted(deleted=bookmark_deleted)


def get_db(
        bookmark_db: AbstractDB = Depends(get_mongo)
) -> BookmarkHandler:
    return BookmarkHandler(MongoDB(bookmark_db))
