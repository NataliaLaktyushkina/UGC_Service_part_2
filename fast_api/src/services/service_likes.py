import abc
from typing import Union

from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from models.likes import MovieRating, LikeUpdated


class AbstractLikeDB(abc.ABC):
    @abc.abstractmethod
    async def add_like(
            self, movie_id: str,
            user_id: str,
            score: int
    ) -> Union[bool, JSONResponse]:
        pass

    @abc.abstractmethod
    async def get_movie_rating(self, movie_id: str) -> MovieRating:
        pass

    @abc.abstractmethod
    async def delete_like(self, movie_id: str, user_id: str) -> Union[bool, JSONResponse]:
        pass

    @abc.abstractmethod
    async def update_like(self, movie_id: str, user_id: str,   # type: ignore
                    score: int, **kwargs) -> Union[LikeUpdated, JSONResponse]:
        pass


class MongoDBLikes(AbstractLikeDB):

    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.ugc_db = self.client.ugc_database
        self.likes_collection = self.ugc_db["likes"]

    async def add_like(
            self, movie_id: str,
            user_id: str, score: int
    ) -> Union[bool, JSONResponse]:
        """Add Like to Mongo DB"""
        like_was_added = await self.do_insert_like(user_id,
                                                   movie_id, score)
        return like_was_added

    async def do_insert_like(
            self, user_id: str,
            movie_id: str,
            score: int
    ) -> Union[bool, JSONResponse]:
        doc = await self.likes_collection.find_one({"movie_id": movie_id,
                                                    "user_id": user_id})
        if doc is None:
            result = await self.likes_collection.insert_one(
                {"movie_id": movie_id,
                 "user_id": user_id,
                 "score": score})

            if result.inserted_id:
                return True
            return JSONResponse(content='Failed to insert like')
        else:
            result = await self.update_like(movie_id=movie_id,
                                            user_id=user_id,
                                            score=score,
                                            document=doc,
                                            )

            return result

    async def get_movie_rating(self, movie_id: str) -> Union[MovieRating, JSONResponse]:

        pipeline = [{"$match":
                         {"movie_id": movie_id},  # noqa E127
                     },
                    {"$group":
                        {
                            "_id": "$movie_id",
                            "avgscore": {"$avg": "$score"},
                        },
                    },
                    ]
        async for doc in self.likes_collection.aggregate(pipeline):
            return MovieRating(movie_id=movie_id,
                               rating=doc["avgscore"])
        return JSONResponse(content='Movie has no rating')

    async def update_like(self, movie_id: str, user_id: str,  # type: ignore
                          score: int, **kwargs) -> Union[LikeUpdated, JSONResponse]:
        if "document" in kwargs:
            doc = kwargs["document"]
        else:
            doc = await self.likes_collection.find_one({"movie_id": movie_id,
                                                        "user_id": user_id})
        if doc is None:
            return JSONResponse(content="Cant find movie_id and/or user_id")
        else:
            doc_id = doc["_id"]
            result = await self.likes_collection.update_one(
                {"_id": doc_id},
                {"$set":
                    {"score": score},
                 })

            if result.modified_count:
                return LikeUpdated(updated=True)
            return LikeUpdated(updated=False)

    async def delete_like(self, movie_id: str, user_id: str) -> Union[bool, JSONResponse]:
        doc = await self.likes_collection.find_one({"movie_id": movie_id,
                                                    "user_id": user_id})
        if doc is None:
            return JSONResponse(content="Movie id was not found")
        else:
            doc_id = doc["_id"]
            result = await self.likes_collection.delete_one(
                {"_id": doc_id})

            if result.deleted_count:
                return True
        return False
