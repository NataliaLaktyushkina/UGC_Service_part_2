from .json_config import BaseOrjsonModel


class BookmarkAdded(BaseOrjsonModel):
    """
        This is the description of event response  model (event accepted or not)
    """
    accepted: bool
