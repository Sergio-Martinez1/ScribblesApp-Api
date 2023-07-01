from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.models import Comment as CommentModel
from schemas.comment import CommentIn, CommentToEdit
from models.models import User as UserModel
from fastapi import HTTPException, status
from datetime import date


class CommentService():

    def __init__(self):
        pass

    async def get_comments(self, db: Session):
        comments = db.query(CommentModel).all()
        if not comments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Comments not found")
        return comments

    async def get_comments_in_post(self, post_id: int, db: Session):
        comments = db.query(CommentModel).filter(
            CommentModel.post_id == post_id).order_by(desc(
                CommentModel.id)).all()
        if not comments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Comments not found in this post")
        return comments

    async def create_comment(self, comment: CommentIn, db: Session,
                             username: str):
        creator = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not creator:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Sign in first")

        new_comment = CommentModel(content=comment.content,
                                   user_id=creator.id,
                                   creation_date=date.today(),
                                   post_id=comment.post_id)
        db.add(new_comment)
        db.commit()
        return

    async def update_comment(self, id: int, new_comment: CommentToEdit,
                             db: Session, username: str):
        comment = db.query(CommentModel).filter(CommentModel.id == id)
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Comment not found")

        creator = db.query(UserModel).filter(
            UserModel.id == comment.first().user_id).first()
        if username != creator.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Operation not allowed")

        comment.update({CommentModel.content: new_comment.content})
        db.commit()
        return

    async def delete_comment(self, id: int, db: Session, username: str):
        comment = db.query(CommentModel).filter(CommentModel.id == id).first()
        if not comment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Comment not found")

        creator = db.query(UserModel).filter(
            UserModel.id == comment.user_id).first()
        if username != creator.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Operation not allowed")

        db.delete(comment)
        db.commit()
        return
