from .json_config import BaseOrjsonModel


class CritiqueAdded(BaseOrjsonModel):
    """
        This is the description of critique post response  model
    """
    added: bool


class CritiqueLiked(BaseOrjsonModel):
    """
        This is the description of add critique like post response  model
    """
    liked: bool


class Critique(BaseOrjsonModel):
    """
        This is the description of get critique's list get response  model
    """
    critique_id: str
    movie_score: int
    critique_rating: float

