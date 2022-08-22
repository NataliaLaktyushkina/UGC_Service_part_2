from fastapi import APIRouter, Depends
from models.bookmarks import BookmarkAdded, BookmarksList, BookmarkDeleted
from services.jwt_check import JWTBearer
from services.bookmarks import BookmarkHandler, get_db

router = APIRouter()


@router.post('/', description="Add bookmark",
             response_description="Movie bookmarked")
async def post_bookmark(movie_id: str,
                        user_id: str = Depends(JWTBearer()),
                        service: BookmarkHandler = Depends(get_db)) -> BookmarkAdded:
    """Add movie to bookmarks"""
    return await service.add_bookmark(movie_id=movie_id,
                                      user_id=user_id)


# deleting a movie from bookmarks
@router.delete('/', description="Delete bookmark",
               response_description="Bookmark removed")
async def delete_bookmark(movie_id: str,
                          user_id: str = Depends(JWTBearer()),
                          service: BookmarkHandler = Depends(get_db)) -> BookmarkDeleted:
    """Delete user's bookmark"""
    return await service.delete_bookmark(movie_id=movie_id,
                                         user_id=user_id)


# view the bookmark list
@router.get('/', description="Show the bookmark list")
async def get_bookmark(
        user_id: str = Depends(JWTBearer()),
        service: BookmarkHandler = Depends(get_db)) -> BookmarksList:
    return await service.get_bookmarks(user_id=user_id)
