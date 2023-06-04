from pydantic import BaseModel, Field


class Tag(BaseModel):
    content: str = Field(default=None)
    post_id: int

    class Config():
        schema_extra = {
            "example": {
                "content": "Movies",
                "post_id": 1
            }
        }
        orm_mode = True
