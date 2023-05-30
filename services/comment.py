from sqlalchemy.orm import Session
from models.models import Comment as CommentModel
from schemas.comment import Comment


class CommentService():
    def __init__(self):
        pass

    async def get_comments(self, db: Session):
        return db.query(CommentModel).all()

    async def create_comment(self, comment: Comment, db: Session):
        new_comment = CommentModel(**comment.dict())
        db.add(new_comment)
        db.commit()
        return

    async def update_comment(self, id: int,  comment: Comment, db: Session):
        comment = db.query(CommentModel).filter(CommentModel.id == id).first()
        comment.update({
            CommentModel.content: Comment.content
        })
        db.commit()
        return

    async def delete_comment(self, id: int, db: Session):
        result = db.query(CommentModel).filter(CommentModel.id == id).first()
        if not result:
            return
        db.delete(result)
        db.commit()
        return
