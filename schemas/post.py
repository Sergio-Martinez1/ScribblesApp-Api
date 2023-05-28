from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .tag import Tag
from .comment import Comment
from .reaction import Reaction


class Post(BaseModel):
    title: str = Field(min_length=4, max_length=30)
    thumbnail: str = Field(None)
    content: str = Field(min_length=20, max_length=300)
    publication_data: datetime = Field(None)
    user_id: int
    tags: List[Tag] = []
    reactions: List[Reaction] = []
    comments: List[Comment] = []
