from sqlalchemy.orm import Session
from models.models import Comment as CommentModel


class CommentService():
    def __init__(self):
        pass

    async def get_comments(self, db: Session):
        return db.query(CommentModel).all()
