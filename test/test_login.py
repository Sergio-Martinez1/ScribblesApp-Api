import httpx
import pytest
from models.models import User
from db_config.database import SessionLocal
from auth.hash_password import HashPassword


@pytest.fixture(scope="module")
async def mock_user() -> User:
    userSchema = User(
        username="sergio",
        email="sergio@mail.com",
        password="123456",
        image="http://image.com",
    )
    hashed_password = HashPassword().create_hash("123456")
    userModel = User(
        username="sergio",
        email="sergio@mail.com",
        password=hashed_password,
        image="http://image.com",
    )
    db = SessionLocal()
    db.add(userModel)
    db.commit()
    db.refresh(userModel)
    yield userSchema


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "pepe",
        "email": "pepe@mail.com",
        "password": "123456",
        "image": "http://image.com"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    test_response = {"message": "User created succesfully."}

    response = await default_client.post("/users/signup",
                                         json=payload,
                                         headers=headers)
    print(response.json().get("detail"))
    assert response.status_code == 201
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_sign_user_in(default_client: httpx.AsyncClient,
                            mock_user: User) -> None:
    payload = {"username": mock_user.username, "password": mock_user.password}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await default_client.post("/users/signin",
                                         data=payload,
                                         headers=headers)
    print(response.json().get("detail"))
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_sign_user_in_with_wrong_username(
        default_client: httpx.AsyncClient, mock_user: User) -> None:
    payload = {"username": "sergio1", "password": mock_user.password}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await default_client.post("/users/signin",
                                         data=payload,
                                         headers=headers)
    print(response.json().get("detail"))
    assert response.status_code == 404
    assert response.json().get("detail") == "User does not exist"


@pytest.mark.asyncio
async def test_sign_user_in_with_wrong_password(
        default_client: httpx.AsyncClient, mock_user: User) -> None:
    payload = {"username": mock_user.username, "password": "1234567"}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = await default_client.post("/users/signin",
                                         data=payload,
                                         headers=headers)
    print(response.json().get("detail"))
    assert response.status_code == 400
    assert response.json().get("detail") == "Incorrect password"
