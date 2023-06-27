from pydantic import BaseModel, Field
from .user import PlainUser
from datetime import date


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
    content: str = Field(default="", max_length=1000)
    creation_date: date = Field(...,
                                example="2023-05-28",
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
