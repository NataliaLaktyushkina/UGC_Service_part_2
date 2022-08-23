from fastapi import APIRouter, Depends, Query

from services.likes import LikesHandler, get_db
from services.jwt_check import JWTBearer
from models.likes import LikeAdded, LikeDeleted, LikeUpdated, MovieRating

router = APIRouter()


@router.post('/', description="Add score",
             response_description="Movie scored")
async def post_score(movie_id: str,
                     score: int = Query(default=0, ge=0, le=10),
                     user_id: str = Depends(JWTBearer()),
                     service: LikesHandler = Depends(get_db)) -> LikeAdded:
    """Add like to movie"""
    return await service.add_like(movie_id=movie_id,
                                  user_id=user_id, score=score)


@router.delete('/', description="Delete score",
               response_description="Score deleted")
async def delete_score(movie_id: str,
                       user_id: str = Depends(JWTBearer()),
                       service: LikesHandler = Depends(get_db)) -> LikeDeleted:
    """Delete movie's score"""
    return await service.delete_like(movie_id=movie_id,
                                     user_id=user_id)


@router.put('/', description="Changing movie's score",
            response_description="Movie's score was updated")
async def change_score(movie_id: str,
                       user_id: str = Depends(JWTBearer()),
                       score: int = Query(default=0, ge=0, le=10),
                       service: LikesHandler = Depends(get_db)) -> LikeUpdated:
    """Changes movie's score"""
    return await service.update_like(movie_id=movie_id,
                                     user_id=user_id,
                                     score=score)


@router.get('/', description="Shows movie's rating",
            response_description="Movie's rating")
async def movies_rating(movie_id: str,
                        user_id: str = Depends(JWTBearer()),
                        service: LikesHandler = Depends(get_db)) -> MovieRating:
    """Get movie's rating"""
    return await service.get_movie_rating(movie_id=movie_id)
