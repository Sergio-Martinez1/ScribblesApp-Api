from sqlalchemy.orm import Session
from models.models import Post as PostModel
from schemas.post import Post, DbPost


class PostService():

    def __init__(self):
        pass

    async def get_posts(self, db: Session):
        return db.query(PostModel).all()

    async def create_post(self, db: Session, post: DbPost):
        new_post = PostModel(title=post.title,
                             thumbnail=post.thumbnail,
                             content=post.content,
                             publication_date=post.publication_date,
                             user_id=post.user_id)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return

    async def update_post(self, db: Session, new_post: Post, id: int):
        post = db.query(PostModel).filter(PostModel.id == id).first()
        post.title = new_post.title
        post.thumbnail = new_post.thumbnail
        post.content = new_post.content
        post.tags = new_post.tags
        db.commit()
        return

    async def delete_post(self, db: Session, id: int):
        post = db.query(PostModel).filter(PostModel.id == id).first()
        if not post:
            return
        db.delete(post)
        db.commit()
