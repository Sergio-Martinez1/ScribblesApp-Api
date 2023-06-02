from models.models import User as UserModel
from schemas.user import User
from sqlalchemy.orm import Session
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from fastapi import HTTPException, status

hash_password = HashPassword()


class UserService():

    def __init__(self):
        pass

    async def get_users(self, db: Session):
        return db.query(UserModel).all()

    async def get_user(self, id: int, db: Session):
        return db.query(UserModel).filter(UserModel.id == id).first()

    async def create_user(self, user: User, db: Session):
        hashed_password = hash_password.create_hash(user.password)
        user.password = hashed_password
        new_user = UserModel(**user.dict())
        db.add(new_user)
        db.commit()
        return

    async def login_user(self, username: str, password: str, db: Session):
        dbUser = db.query(UserModel).filter(
            UserModel.username == username).first()

        if not dbUser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exist")

        if hash_password.verify_hash(password, dbUser.password):
            access_token = create_access_token(dbUser.username)
            return {
                "access_token": access_token,
                "token_type": "Bearer",
                "user_id": dbUser.id,
                "username": dbUser.username
            }
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Incorrect password")
