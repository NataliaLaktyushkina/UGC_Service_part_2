from .json_config import BaseOrjsonModel
from typing import Dict


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
    critique_id: str
    movie_score: int


class CritiqueList(BaseOrjsonModel):
    """
        This is the description of get critique's list get response  model
    """
    movie_id: str
    critique: Critique

