from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from schemas.user import NewUser, MyUser, PublicUser, UserUpdate, PlainMyUser
from schemas.user import PasswordChange, UsernameChange
from schemas.user import TokenResponse
from sqlalchemy.orm import Session
from db_config.database import get_db
from services.user import UserService
from fastapi.security import OAuth2PasswordRequestForm
from auth.authenticate import authenticate

users_route = APIRouter(prefix='/users', tags=['user'])


@users_route.get("/all",
                 response_model=List[PublicUser],
                 status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)) -> List[PublicUser]:
    users = await UserService().get_users(db)
    return users


@users_route.get("/myUser",
                 response_model=MyUser,
                 status_code=status.HTTP_200_OK)
async def get_my_user(db: Session = Depends(get_db),
                      user: str = Depends(authenticate)) -> MyUser:
    myUser = await UserService().get_my_user(user, db)
    return myUser


@users_route.get("/plainMyUser",
                 response_model=PlainMyUser,
                 status_code=status.HTTP_200_OK)
async def get_plain_my_user(db: Session = Depends(get_db),
                            user: str = Depends(authenticate)) -> PlainMyUser:
    plainMyUser = await UserService().get_plain_my_user(user, db)
    return plainMyUser


@users_route.get("/{id}",
                 response_model=PublicUser,
                 status_code=status.HTTP_200_OK)
async def get_user(id: int, db: Session = Depends(get_db)) -> PublicUser:
    user = await UserService().get_user(id, db)
    return user


@users_route.delete("/", status_code=status.HTTP_200_OK)
async def delete_user(db: Session = Depends(get_db),
                      user: str = Depends(authenticate)) -> dict:
    await UserService().delete_user(user, db)
    return JSONResponse(content={'message': 'User deleted succesfully'},
                        status_code=status.HTTP_200_OK)


@users_route.post('/signup',
                  status_code=status.HTTP_201_CREATED,
                  response_model=dict)
async def sign_user_up(user: NewUser, db: Session = Depends(get_db)) -> dict:

    await UserService().create_user(user, db)
    return JSONResponse(content={"message": "User created succesfully."},
                        status_code=status.HTTP_201_CREATED)


@users_route.put('/update',
                 status_code=status.HTTP_200_OK,
                 response_model=dict)
async def user_update(
    request: UserUpdate,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate)
) -> dict:
    await UserService().update_user(request, user, db)
    return JSONResponse(content={"message": "User updated succesfully."},
                        status_code=status.HTTP_201_CREATED)


@users_route.post('/signin', response_model=TokenResponse)
async def sign_user_in(request: OAuth2PasswordRequestForm = Depends(),
                       db: Session = Depends(get_db)) -> TokenResponse:

    return await UserService().login_user(request.username, request.password,
                                          db)


@users_route.put('/password', response_model=dict)
async def password_change(
    password: PasswordChange,
    db: Session = Depends(get_db),
    username: str = Depends(authenticate)
) -> dict:
    await UserService().change_password(username, password.password,
                                        password.new_password, db)
    return JSONResponse(content={"message": "Password changed succesfully."},
                        status_code=status.HTTP_200_OK)


@users_route.put('/username', response_model=dict)
async def username_change(
    new_username: UsernameChange,
    db: Session = Depends(get_db),
    username: str = Depends(authenticate)
) -> dict:
    await UserService().change_username(username, new_username.username,
                                        new_username.password, db)
    return JSONResponse(content={"message": "Username changed succesfully."},
                        status_code=status.HTTP_200_OK)
