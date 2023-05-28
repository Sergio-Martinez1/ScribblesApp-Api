from sqlalchemy.orm import Session
from models.models import Tag as TagModel


class TagService():
    def __init__(self):
        pass

    async def get_tags(self, db: Session):
        return db.query(TagModel).all()
