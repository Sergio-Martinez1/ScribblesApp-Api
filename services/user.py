from models.models import User as UserModel
from schemas.user import NewUser, MyUser, UserUpdate
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

    async def get_plain_my_user(self, username: str, db: Session):
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

        email = db.query(UserModel).filter(
            UserModel.email == request.email).first()

        if email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already exist")

        hashed_password = hash_password.create_hash(request.password)
        request.password = hashed_password
        new_user = UserModel(**request.dict(), creation_date=date.today())
        db.add(new_user)
        db.commit()
        return

    async def update_user(self, request: UserUpdate, username: str,
                          db: Session):
        user = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exist")

        if request.email is not None:
            user.email = request.email
        if request.profile_photo is not None:
            user.profile_photo = request.profile_photo
        if request.cover_photo is not None:
            user.cover_photo = request.cover_photo
        if request.description is not None:
            user.description = request.description
        if request.personal_url is not None:
            user.personal_url = request.personal_url
        if request.location is not None:
            user.location = request.location
        if request.birthday is not None:
            user.birthday = request.birthday
        db.add(user)
        db.commit()
        db.refresh(user)
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

    async def change_username(self, username: str, new_username: str,
                              password: str, db: Session):
        user = db.query(UserModel).filter(
            UserModel.username == new_username).first()

        if user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username already exist")
        user = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does not exist")
        if not hash_password.verify_hash(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect password")
        if new_username is not None:
            user.username = new_username
        db.add(user)
        db.commit()
        db.refresh(user)
        return
