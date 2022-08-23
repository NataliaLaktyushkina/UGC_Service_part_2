from .json_config import BaseOrjsonModel


class LikeAdded(BaseOrjsonModel):
    """
        This is the description of likes post response  model
    """
    added: bool


class LikeUpdated(BaseOrjsonModel):
    """
        This is the description of likes put response  model
    """
    updated: bool


class MovieRating(BaseOrjsonModel):
    """
        This is the description of likes list response  model
    """
    movie_id: str
    rating: float


class LikeDeleted(BaseOrjsonModel):
    """
            This is the description of like delete response  model
    """
    deleted: bool
