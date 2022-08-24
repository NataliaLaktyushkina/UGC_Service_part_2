from fastapi import Depends
from fastapi.responses import JSONResponse
from services.service_likes import AbstractLikeDB, MongoDBLikes
from db.mongo_db import get_mongo
from models.likes import LikeAdded, LikeDeleted, LikeUpdated, MovieRating
from typing import Union


class LikesHandler:
    def __init__(self, likes_db: AbstractLikeDB):
        self.likes_db = likes_db

    async def add_like(self, movie_id: str, user_id: str, score: int) -> LikeAdded:
        like_added = await self.likes_db.add_like(movie_id, user_id, score)
        return LikeAdded(added=like_added)

    async def get_movie_rating(self, movie_id: str) -> MovieRating:
        return await self.likes_db.get_movie_rating(movie_id)

    async def delete_like(self, movie_id: str, user_id: str) -> LikeDeleted:
        like_deleted = await self.likes_db.delete_like(movie_id, user_id)
        return LikeDeleted(deleted=like_deleted)

    async def update_like(self, movie_id: str, user_id: str, score: int) -> Union[LikeUpdated, JSONResponse]:
        like_updated = await self.likes_db.update_like(movie_id, user_id, score)
        return like_updated


def get_db(
        likes_db: AbstractLikeDB = Depends(get_mongo)
) -> LikesHandler:
    return LikesHandler(MongoDBLikes(likes_db))
