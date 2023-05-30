from pydantic import BaseModel


class Reaction(BaseModel):
    id: int
    user_id: int

    class Config():
        orm_mode = True
