from sqlalchemy.orm import Session
from models.models import Reaction as ReactionModel


class ReactionService():
    def __init__(self):
        pass

    async def get_reactions(self, db: Session):
        return db.query(ReactionModel).all()
