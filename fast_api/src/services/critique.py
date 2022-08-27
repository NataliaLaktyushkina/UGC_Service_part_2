from typing import Union, List

from fastapi import Depends
from fastapi.responses import JSONResponse

from db.mongo_db import get_mongo
from models.critique import CritiqueAdded, CritiqueLiked, Critique
from services.service_critique import AbstractCritiqueDB, MongoDBCritique


class CritiqueHandler:
    def __init__(self, critique_db: AbstractCritiqueDB):
        self.critique_db = critique_db

    async def add_critique(self, movie_id: str, user_id: str,
                           movie_score: int, text: str) -> Union[CritiqueAdded, JSONResponse]:
        critique_added = await self.critique_db.add_critique(movie_id, user_id,
                                                             movie_score, text)
        return critique_added

    async def add_like(self, critique_id: str,
                       user_id: str, like: int) -> Union[CritiqueLiked, JSONResponse]:
        like_added = await self.critique_db.add_critique_like(critique_id, user_id,
                                                              like)
        return like_added

    async def get_list(self, movie_id: str) -> List[Critique]:
        return await self.critique_db.get_critique_list(movie_id=movie_id)


def get_db(
        critique_db: AbstractCritiqueDB = Depends(get_mongo)
) -> CritiqueHandler:
    return CritiqueHandler(MongoDBCritique(critique_db))
