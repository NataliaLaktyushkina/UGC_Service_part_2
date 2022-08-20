from fastapi import APIRouter, Depends
from models.bookmarks import BookmarkAdded
from services.jwt_check import JWTBearer


router = APIRouter()


# add movie to bookmarks;
@router.post('/', description="Add bookmark",
             response_description="Movie bookmarked")
async def post_bookmark(movie_id: str,
                        user_id: str = Depends(JWTBearer()),) -> BookmarkAdded:
    return await



# deleting a movie from bookmarks
@router.delete('/', description="Delete bookmark",
             response_description="Bookmark removed")
async def delete_bookmark():
    pass

# view the bookmark list
@router.get('/', description="Show the bookmark list")
async def get_bookmark():
    pass
