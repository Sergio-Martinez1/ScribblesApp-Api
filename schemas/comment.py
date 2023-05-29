from pydantic import BaseModel, Field


class Comment(BaseModel):
    content: str = Field(default="", max_length=1000)
    user_id: int

    class Config():
        schema_extra = {
            "example": {
                "content": "Some content for a comment",
            }
        }
        orm_mode = True
