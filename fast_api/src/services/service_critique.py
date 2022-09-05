import abc
from datetime import datetime
from typing import Union, List

from fastapi.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from models.critique import CritiqueAdded, CritiqueLiked, Critique, DropDownSorting


class AbstractCritiqueDB(abc.ABC):
    @abc.abstractmethod
    def add_critique(self, movie_id: str, user_id: str,
                     movie_score: int, text: str) -> Union[CritiqueAdded, JSONResponse]:
        pass

    @abc.abstractmethod
    def add_critique_like(self, critique_id: str, user_id: str,
                          like: int) -> CritiqueLiked:
        pass

    @abc.abstractmethod
    def get_critique_list(self, movie_id: str, sorting_type: str) -> Critique:
        pass


class MongoDBCritique(AbstractCritiqueDB):

    def __init__(self, client: AsyncIOMotorClient):
        self.client = client
        self.ugc_db = self.client.ugc_database
        self.critique_collection = self.ugc_db["critique"]
        self.critique_likes_collection = self.ugc_db["critique_likes"]

    async def add_critique(self, movie_id: str, user_id: str,
                           movie_score: int, text: str) -> Union[CritiqueAdded, JSONResponse]:
        """Add critique to Mongo DB"""
        critique_was_added = await self.do_insert_critique(user_id, movie_id,
                                                           movie_score, text)
        return critique_was_added

    async def do_insert_critique(self, user_id: str,
                                 movie_id: str,
                                 movie_score: int, text: str) -> Union[CritiqueAdded, JSONResponse]:
        doc = await self.critique_collection.find_one({"movie_id": movie_id,
                                                       "user_id": user_id})
        if doc is None:
            result = await self.critique_collection.insert_one(
                {"movie_id": movie_id,
                 "user_id": user_id,
                 "movie_score": movie_score,
                 "text": text,
                 "timestamp": datetime.now()},
            )

            if result.inserted_id:
                return CritiqueAdded(added=True)
        else:
            return JSONResponse(content="You've already added review to current movie")

    async def add_critique_like(self, critique_id: str, user_id: str,
                                like: int) -> CritiqueLiked:
        """Add like/dislike to critique in Mongo DB"""
        critique_liked = await self.insert_critique_like(critique_id,
                                                         user_id, like)
        return critique_liked

    async def insert_critique_like(self, critique_id: str,
                                   user_id: str, like: int) -> CritiqueLiked:
        doc = await self.critique_likes_collection.find_one({"critique_id": critique_id,
                                                             "user_id": user_id})
        if doc is None:
            result = await self.critique_likes_collection.insert_one(
                {"critique_id": critique_id,
                 "user_id": user_id,
                 "like": like,
                 })

            if result.inserted_id:
                return CritiqueLiked(liked=True)
        else:
            # update
            result = await self.update_like(critique_id=critique_id,
                                            user_id=user_id,
                                            like=like,
                                            )

            return result

    async def update_like(self, critique_id: str, user_id: str, like: int) -> Union[JSONResponse, CritiqueLiked]:

        doc = await self.critique_likes_collection.find_one({"critique_id": critique_id,
                                                             "user_id": user_id})
        if doc is None:
            return JSONResponse(content="Cant find critique_id nd/or user_id")
        else:
            doc_id = doc["_id"]
            result = await self.critique_likes_collection.update_one(
                {"_id": doc_id},
                {"$set":
                     {"like": like},
                 })

            if result.modified_count:
                return CritiqueLiked(liked=True)
            return CritiqueLiked(liked=False)

    async def get_critique_list(self, movie_id: str,
                                sorting_type: DropDownSorting) -> List[Critique]:
        critique_list = []
        pipeline = [
            {"$match":
                 {"movie_id": movie_id},
             }]
        if sorting_type == DropDownSorting.by_date:
            pipeline.append(
                {"$sort":
                     {"timestamp": -1},
                 })

        async for doc in self.critique_collection.aggregate(pipeline):
            rating_pipeline = [{"$match":
                                    {"critique_id": str(doc["_id"])},
                                },
                               {"$group":
                                   {
                                       "_id": "$critique_id",
                                       "rating": {"$sum": "$like"},
                                   },
                               },
                               ]

            async for res in self.critique_likes_collection.aggregate(rating_pipeline):
                critique_list.append({"critique_id": doc["_id"],
                                      "movie_score": doc["movie_score"],
                                      "critique_rating": res["rating"],
                                      "creation_date": doc["timestamp"]})
        if sorting_type == DropDownSorting.by_rating:
            sorted_critique = sorted(critique_list,
                                     key=lambda r: r["critique_rating"], reverse=True)
        elif sorting_type == DropDownSorting.by_date:
            sorted_critique = sorted(critique_list,
                                     key=lambda r: r["creation_date"], reverse=True)
        return [Critique(critique_id=str(cl["critique_id"]),
                         movie_score=cl["movie_score"],
                         critique_rating=cl["critique_rating"],
                         creation_date=cl["creation_date"]) for cl in sorted_critique]
