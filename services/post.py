from sqlalchemy.orm import Session
from models.models import Post as PostModel
from models.models import User as UserModel
from schemas.post import PostIn
from fastapi import HTTPException, status
from datetime import date


class PostService():

    def __init__(self):
        pass

    async def get_posts(self, db: Session):
        return db.query(PostModel).all()

    async def create_post(self, db: Session, post: PostIn, username: str):
        # Request the user id in the database
        creator = db.query(UserModel).filter(
            UserModel.username == username).first()
        # Validate that the user exist
        if not creator:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found, sign in again")

        # Filling the fields for the database post model
        new_post = PostModel(title=post.title,
                             thumbnail=post.thumbnail,
                             content=post.content,
                             publication_date=date.today(),
                             user_id=creator.id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return

    async def update_post(self, db: Session, new_post: PostIn, id: int,
                          username: str):
        post = db.query(PostModel).filter(PostModel.id == id).first()
        creator = db.query(UserModel).filter(
            UserModel.id == post.user_id).first()
        if username != creator.username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Operation not allowed")
        post.title = new_post.title
        post.thumbnail = new_post.thumbnail
        post.content = new_post.content
        post.tags = new_post.tags
        db.commit()
        return

    async def delete_post(self, db: Session, id: int, username: str):
        post = db.query(PostModel).filter(PostModel.id == id).first()
        creator = db.query(UserModel).filter(
            UserModel.id == post.user_id).first()
        if username != creator.username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Operation not allowed")
        post = db.query(PostModel).filter(PostModel.id == id).first()
        if not post:
            return
        db.delete(post)
        db.commit()
