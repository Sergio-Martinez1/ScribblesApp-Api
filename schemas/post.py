from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .tag import Tag
from .reaction import ReactionOut
from .user import PlainUser


class PostOut(BaseModel):
    id: int
    content: str = Field(None, min_length=1, max_length=1000)
    thumbnail: str = Field(None)
    publication_date: datetime = Field(
        ...,
        example="2024-03-22T01:50:25.664273+00:00",
        description="My date field")
    user_id: int
    user: PlainUser
    reactions: List[ReactionOut] = []
    tags: List[Tag] = []
    num_comments: int

    class Config():
        orm_mode = True


class PostIn(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    thumbnail: Optional[str] = None
    tags: Optional[List[str]] = []

    class Config():
        orm_mode = True
