from typing import List

from fastapi import APIRouter, Depends, Query

from models.critique import CritiqueAdded, CritiqueLiked, Critique
from services.critique import CritiqueHandler, get_db
from services.jwt_check import JWTBearer

router = APIRouter()


@router.post('/', description="Add a movie review",
             response_description="Review added")
async def post_critique(movie_id: str,
                        text: str,
                        user_id: str = Depends(JWTBearer()),
                        movie_score: int = Query(default=0, ge=0, le=10),
                        service: CritiqueHandler = Depends(get_db)) -> CritiqueAdded:
    """Add critique to movie"""
    return await service.add_critique(movie_id=movie_id,
                                      user_id=user_id,
                                      movie_score=movie_score,
                                      text=text)


@router.post('/like', description="Add critique like",
             response_description="Like added")
async def post_critique_like(critique_id: str,
                             like: int = Query([-1, 1]),
                             user_id: str = Depends(JWTBearer()),
                             service: CritiqueHandler = Depends(get_db)) -> CritiqueLiked:
    """Add critique to movie"""
    return await service.add_like(critique_id=critique_id,
                                  user_id=user_id,
                                  like=like)


@router.get('/', description="Get movie's critique list",
            response_description="Provided movie's critique list")
async def get_critique_list(movie_id: str,
                            user_id: str = Depends(JWTBearer()),
                            service: CritiqueHandler = Depends(get_db)) -> List[Critique]:
    """Get movie's critique list with sorting"""
    return await service.get_list(movie_id=movie_id)
