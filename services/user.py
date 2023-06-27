from models.models import User as UserModel
from schemas.user import NewUser, MyUser
from sqlalchemy.orm import Session
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from fastapi import HTTPException, status
from datetime import date

hash_password = HashPassword()


class UserService():

    def __init__(self):
        pass

    async def get_users(self, db: Session):
        users = db.query(UserModel).all()

        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No users found")
        return users

    async def get_my_user(self, username: str, db: Session):
        user = db.query(UserModel).filter(
            UserModel.username == username).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exits")
        return user

    async def get_user(self, id: int, db: Session):
        user = db.query(UserModel).filter(UserModel.id == id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exist")
        return user

    async def create_user(self, request: NewUser, db: Session):
        user = db.query(UserModel).filter(
            UserModel.username == request.username).first()

        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username already exist")

        hashed_password = hash_password.create_hash(request.password)
        request.password = hashed_password
        new_user = UserModel(**request.dict(), creation_date=date.today())
        db.add(new_user)
        db.commit()
        return

    async def delete_user(self, username: str, db: Session):
        user_exist = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user_exist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exist")

        db.delete(user_exist)
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
                "username": dbUser.username,
                "profile_photo": dbUser.profile_photo
            }
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect password")
        return

    async def change_password(self, username: str, password: str,
                              new_password: str, db: Session):
        dbUser = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not dbUser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exist")
        if hash_password.verify_hash(password, dbUser.password):
            hashed_password = hash_password.create_hash(new_password)
            dbUser.password = hashed_password
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Incorrect password")
        return
