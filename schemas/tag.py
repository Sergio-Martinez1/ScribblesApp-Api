from pydantic import BaseModel, Field


class Tag(BaseModel):
    id: int
    content: str = Field(default=None)

    class Config():
        schema_extra = {
            "example": {
                "content": "Movies",
            }
        }
        orm_mode = True
