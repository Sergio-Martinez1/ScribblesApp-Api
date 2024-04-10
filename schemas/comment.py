from pydantic import BaseModel, Field
from .user import PlainUser
from datetime import datetime


class CommentIn(BaseModel):
    content: str = Field(default="", max_length=1000)
    post_id: int

    class Config():
        schema_extra = {
            "example": {
                "content": "Some content for a comment",
                "post_id": 1
            }
        }
        orm_mode = True


class CommentToEdit(BaseModel):
    content: str = Field(default="", max_length=1000)

    class Config():
        schema_extra = {
            "example": {
                "content": "Some content for a comment",
            }
        }
        orm_mode = True


class CommentOut(BaseModel):
    id: int
    content: str = Field(default="", max_length=1000)
    creation_date: datetime = Field(...,
                                    example="2024-03-22T01:50:25.664273+00:00",
                                    description="My date field")
    post_id: int
    user_id: int
    user: PlainUser

    class Config():
        schema_extra = {
            "example": {
                "content": "Some content for a comment",
                "post_id": 1,
                "user_id": 1
            }
        }
        orm_mode = True
