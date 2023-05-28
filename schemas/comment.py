from pydantic import BaseModel, Field


class Comment(BaseModel):
    content: str = Field(default="", max_length=200)

    class Config():
        schema_extra = {
            "example": "This is a comment example"
        }
        orm_mode = True
