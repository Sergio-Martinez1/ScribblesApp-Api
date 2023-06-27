from pydantic import BaseModel, Field
from typing import List
from datetime import date
from .tag import Tag
from schemas.comment import CommentOut
from .reaction import Reaction
from .user import PlainUser


class PostOut(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
    thumbnail: str = Field(None)
    publication_date: date = Field(...,
                                   example="2023-05-28",
                                   description="My date field")
    user_id: int
    user: PlainUser
    reactions: List[Reaction] = []
    comments: List[CommentOut] = []
    tags: List[Tag] = []

    class Config():
        orm_mode = True


class PostIn(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
    thumbnail: str = Field(None)
    tags: List[Tag] = []

    class Config():
        orm_mode = True
