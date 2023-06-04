from pydantic import BaseModel, Field
from typing import List
from datetime import date
from .tag import Tag
from schemas.comment import CommentOut
from .reaction import Reaction


class PostOut(BaseModel):
    title: str = Field(min_length=1, max_length=1000)
    thumbnail: str = Field(None)
    content: str = Field(min_length=1, max_length=1000)
    publication_date: date = Field(...,
                                   example="2023-05-28",
                                   description="My date field")
    user_id: int
    tags: List[Tag] = []
    reactions: List[Reaction] = []
    comments: List[CommentOut] = []

    class Config():
        orm_mode = True


class PostIn(BaseModel):
    title: str = Field(min_length=1, max_length=1000)
    thumbnail: str = Field(None)
    content: str = Field(min_length=1, max_length=1000)
    tags: List[Tag] = []

    class Config():
        orm_mode = True
