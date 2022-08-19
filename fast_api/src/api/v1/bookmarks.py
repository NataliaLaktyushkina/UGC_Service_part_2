from fastapi import APIRouter


router = APIRouter()


@router.post('/', description="Add bookmark",
             response_description="Bookmark was added")
async def post_bookmark():
    pass
