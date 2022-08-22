from fastapi import Depends
from services.service import AbstractDB, MongoDB
from db.mongo_db import get_mongo


class LikesHandler:
    def __init__(self, likes_db: AbstractDB):
        self.likes_db = likes_db

    async def add_like(self, movie_id: str, user_id: str) -> BookmarkAdded:
        bookmark_added = await self.bookmark_db.add_bookmark(movie_id, user_id)
        return BookmarkAdded(added=bookmark_added)

    async def get_movie_rating(self, movie_id: str) -> BookmarksList:
        return await self.bookmark_db.get_bookmarks_list(user_id)

    async def delete_like(self, movie_id: str, user_id: str) -> BookmarkDeleted:
        bookmark_deleted = await self.bookmark_db.delete_bookmark(movie_id, user_id)
        return BookmarkDeleted(deleted=bookmark_deleted)

    async def update_like(self, movie_id: str, user_id: str):
       pass


def get_db(
        likes_db: AbstractDB = Depends(get_mongo)
) -> LikesHandler:
    return LikesHandler(MongoDB(likes_db))
