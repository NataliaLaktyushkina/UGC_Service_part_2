from typing import Union

from fastapi import Depends
from fastapi.responses import JSONResponse

from db.mongo_db import get_mongo
from models.critique import CritiqueAdded
from services.service import AbstractCritiqueDB, MongoDBCritique


class CritiqueHandler:
    def __init__(self, critique_db: AbstractCritiqueDB):
        self.critique_db = critique_db

    async def add_critique(self, movie_id: str, user_id: str,
                           movie_score: int, text: str) -> Union[CritiqueAdded, JSONResponse]:
        like_added = await self.critique_db.add_critique(movie_id, user_id,
                                                         movie_score,text)
        return like_added


def get_db(
        critique_db: AbstractCritiqueDB = Depends(get_mongo)
) -> CritiqueHandler:
    return CritiqueHandler(MongoDBCritique(critique_db))
