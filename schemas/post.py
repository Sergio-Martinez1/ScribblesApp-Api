from pydantic import BaseModel, Field
from typing import List
from datetime import date
from .tag import Tag
from .comment import Comment
from .reaction import Reaction


class Post(BaseModel):
    title: str = Field(min_length=1, max_length=1000)
    thumbnail: str = Field(None)
    content: str = Field(min_length=1, max_length=1000)
    publication_date: date = Field(...,
                                   example="2023-05-28",
                                   description="My date field")
    user_id: int
    tags: List[Tag] = []
    reactions: List[Reaction] = []
    comments: List[Comment] = []

    class Config():
        orm_mode = True


class DbPost(BaseModel):
    title: str = Field(min_length=1, max_length=1000)
    thumbnail: str = Field(None)
    content: str = Field(min_length=1, max_length=1000)
    publication_date: date = Field(...,
                                   example="2023-05-28",
                                   description="My date field")
    user_id: int

    class Config():
        orm_mode = True
