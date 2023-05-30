from sqlalchemy.orm import Session
from models.models import Tag as TagModel
from schemas.tag import Tag


class TagService():
    def __init__(self):
        pass

    async def get_tags(self, db: Session):
        return db.query(TagModel).all()

    async def create_tag(self, tag: Tag, db: Session):
        new_tag = TagModel(**tag.dict())
        db.add(new_tag)
        db.commit()
        return

    async def delete_tag(self, id: int, db: Session):
        result = db.query(TagModel).filter(TagModel.id == id).first()
        if not result:
            return
        db.delete(result)
        db.commit()
        return
