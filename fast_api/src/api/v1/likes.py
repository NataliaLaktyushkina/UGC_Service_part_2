from fastapi import APIRouter, Depends

from services.likes import LikesHandler, get_db
from services.jwt_check import JWTBearer
from models.likes import LikeAdded

router = APIRouter()


@router.post('/', description="Add score",
             response_description="Movie scored")
async def post_score(movie_id: str,
                     user_id: str = Depends(JWTBearer()),
                     service: LikesHandler = Depends(get_db)) -> LikeAdded:
    """Add like to movie"""
    return await service.add_like(movie_id=movie_id,
                                  user_id=user_id)


@router.delete('/', description="Delete score",
               response_description="Score deleted")
async def delete_score():
    """Delete movie's score"""
    pass


@router.put('/', description="Changing movie's score",
            response_description="Movie's score was updated")
async def change_score():
    """Changes movie's score"""
    pass


@router.get('/', description="Shows movie's rating",
            response_description="Movie's rating")
async def movies_rating():
    """Get movie's rating"""
    pass
