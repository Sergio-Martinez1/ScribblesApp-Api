import httpx
import pytest
from models.models import Post
from db_config.database import SessionLocal
from models.models import User
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from datetime import date


@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("sergio")


@pytest.fixture(scope="module")
async def mock_user() -> User:
    test_password = "123456"
    hashed_password = HashPassword().create_hash(test_password)
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
    stored_user = db.query(User).filter(
        User.username == userModel.username).first()
    yield stored_user


@pytest.fixture(scope="module")
async def mock_post(mock_user: User) -> Post:
    new_post = Post(title="Title for a test post",
                    thumbnail="http://image.com",
                    content="Some content for a test post",
                    publication_date=date.today(),
                    user_id=mock_user.id)
    db = SessionLocal()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    stored_post = db.query(Post).filter(Post.user_id == mock_user.id).first()
    yield stored_post


@pytest.mark.asyncio
async def test_get_posts(default_client: httpx.AsyncClient,
                         mock_post: Post) -> None:
    response = await default_client.get("/posts/")
    assert response.status_code == 200
    # assert response.json()[2]["title"] == str(mock_post.title)


@pytest.mark.asyncio
async def test_get_single_post(default_client: httpx.AsyncClient,
                               mock_post: Post) -> None:
    response = await default_client.get(f"/posts/{mock_post.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_post(default_client: httpx.AsyncClient,
                           access_token: str) -> None:
    payload = {
        "title": "Test Post",
        "thumbnail": "https://fakeimagepost.com",
        "content": "Testing the POST method for posts",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {'message': 'Post sucessfully created'}

    response = await default_client.post("/posts/",
                                         json=payload,
                                         headers=headers)
    assert response.status_code == 201
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_update_post(default_client: httpx.AsyncClient,
                           access_token: str, mock_post: Post) -> None:
    payload = {
        "title": "Updated Post",
        "thumbnail": "https://newimage.com",
        "content": "Testing the PUT method for posts",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {'message': 'Post sucessfully updated'}

    response = await default_client.put(f"/posts/{mock_post.id}",
                                        json=payload,
                                        headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_delete_post(default_client: httpx.AsyncClient,
                           access_token: str, mock_post: Post) -> None:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {'message': 'Post sucessfully deleted'}

    response = await default_client.delete(f"/posts/{mock_post.id}",
                                           headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response
