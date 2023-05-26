from models.user import User as UserModel
from schemas.user import User
from sqlalchemy.orm import Session


class UserService():

    def __init__(self):
        pass

    async def get_users(self, db: Session):
        return db.query(UserModel).all()

    async def get_user(self, id: int, db: Session):
        return db.query(UserModel).filter(UserModel.id == id).first()

    async def create_user(self, user: User, db: Session):
        new_user = UserModel(**user.dict())
        db.add(new_user)
        db.commit()
