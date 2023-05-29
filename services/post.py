from sqlalchemy.orm import Session
from models.models import Post as PostModel


class PostService():
    def __init__(self):
        pass

    async def get_posts(self, db: Session):
        return db.query(PostModel).all()
