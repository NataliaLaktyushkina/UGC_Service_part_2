from fastapi import Depends
from services.service import AbstractLikeDB
from db.mongo_db import get_mongo
from models.likes import LikeAdded, LikeDeleted, LikeUpdated, MovieRating


class LikesHandler:
    def __init__(self, likes_db: AbstractLikeDB):
        self.likes_db = likes_db

    async def add_like(self, movie_id: str, user_id: str) -> LikeAdded:
        like_added = await self.likes_db.add_like(movie_id, user_id)
        return LikeAdded(added=like_added)

    async def get_movie_rating(self, movie_id: str) -> MovieRating:
        return await self.likes_db.get_movie_rating(movie_id)

    async def delete_like(self, movie_id: str, user_id: str) -> LikeDeleted:
        like_deleted = await self.likes_db.delete_like(movie_id, user_id)
        return LikeDeleted(deleted=like_deleted)

    async def update_like(self, movie_id: str, user_id: str) -> LikeUpdated:
        like_updated = await self.likes_db.update_like(movie_id, user_id)
        return LikeUpdated(updated=like_updated)


def get_db(
        likes_db: AbstractLikeDB = Depends(get_mongo)
) -> LikesHandler:
    return LikesHandler(AbstractLikeDB(likes_db))
