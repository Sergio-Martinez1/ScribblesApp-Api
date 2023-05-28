from pydantic import BaseModel, Field


class Reaction(BaseModel):
    id: int

    class Config():
        orm_mode = True
