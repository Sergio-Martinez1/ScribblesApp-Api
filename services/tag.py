from sqlalchemy.orm import Session
from models.models import Tag as TagModel
from schemas.tag import Tag
from models.models import User as UserModel
from fastapi import HTTPException, status
from sqlalchemy import func


class TagService():

    def __init__(self):
        pass

    async def get_tags(self, db: Session):
        tags = db.query(TagModel).all()

        if not tags:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No tags found")
        return tags

    async def get_top_tags(self, db: Session, limit: int = 3):
        tags = db.query(TagModel.content, func.count(TagModel.post_id).label('count')).\
            group_by(TagModel.content).\
            order_by(func.count(TagModel.post_id).desc()).\
            limit(limit).\
            all()
        if not tags:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No tags found")
        tag_data = []
        for tag in tags:
            tag_data.append({"content": tag[0], "count": tag[1]})
        return tag_data

    async def create_tag(self, tag: Tag, db: Session, username: str):
        user_exist = db.query(UserModel).filter(
            UserModel.username == username).first()

        if not user_exist:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Sign in first")

        new_tag = TagModel(**tag.dict())
        db.add(new_tag)
        db.commit()
        return

    async def delete_tag(self, id: int, db: Session, username: str):
        user_exist = db.query(UserModel).filter(
            UserModel.username == username).first()

        if not user_exist:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Sign in first")

        result = db.query(TagModel).filter(TagModel.id == id).first()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Tag not found")
        db.delete(result)
        db.commit()
        return
