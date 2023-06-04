from pydantic import BaseModel, Field


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
    post_id: int
    user_id: int

    class Config():
        schema_extra = {
            "example": {
                "content": "Some content for a comment",
                "post_id": 1,
                "user_id": 1
            }
        }
        orm_mode = True
