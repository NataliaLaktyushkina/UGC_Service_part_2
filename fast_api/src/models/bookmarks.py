from .json_config import BaseOrjsonModel
from typing import List


class BookmarkAdded(BaseOrjsonModel):
    """
        This is the description of bookmarks post response  model
    """
    added: bool


class BookmarksList(BaseOrjsonModel):
    """
        This is the description of bookmarks list response  model
    """
    movie_id: List[str]
