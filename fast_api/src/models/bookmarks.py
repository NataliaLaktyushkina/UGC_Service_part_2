from .json_config import BaseOrjsonModel


class BookmarkAdded(BaseOrjsonModel):
    """
        This is the description of bookmarks post response  model
    """
    added: bool


class BookmarksList(BaseOrjsonModel):
    """
        This is the description of bookmarks list response  model
    """
    movie_id: list[str]  # type: ignore


class BookmarkDeleted(BaseOrjsonModel):
    """
            This is the description of bookmarks delete response  model
    """
    deleted: bool
