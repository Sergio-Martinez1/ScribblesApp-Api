import httpx
import pytest
from models.models import Post
from db_config.database import SessionLocal
from models.models import User
from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token


@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("mutska")


@pytest.fixture(scope="module")
async def mock_user() -> User:
    hashed_password = HashPassword().create_hash("fakepassword")
    userModel = User(
        username="mutska",
        email="mutska@mail.com",
        password=hashed_password,
        image="http://image.com",
    )
    db = SessionLocal()
    db.add(userModel)
    db.commit()
    db.refresh(userModel)
    db.close()
    yield userModel


@pytest.fixture(scope="module")
async def mock_post(mock_user: User) -> Post:
    db = SessionLocal()
    post_to_update = Post(
        title="Post to Update",
        thumbnail="https://fakeimage.com",
        content="This a post to update",
        publication_date="2023-06-01",
        user_id=1
    )
    db.add(post_to_update)
    db.commit()
    db.refresh(post_to_update)

    post_to_delete = Post(
        title="Post to delete",
        thumbnail="https://fakeimage.com",
        content="This a post to delete",
        publication_date="2023-06-01",
        user_id=1
    )
    db.add(post_to_delete)
    db.commit()
    db.refresh(post_to_delete)

    new_post = Post(
        title="Test Post",
        thumbnail="https://fakeimage.com",
        content="This a test post",
        publication_date="2023-06-01",
        user_id=1
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    db.close()
    yield new_post


@pytest.mark.asyncio
async def test_get_posts(default_client: httpx.AsyncClient,
                         mock_post: Post) -> None:
    response = await default_client.get("/posts/")
    assert response.status_code == 200
    assert response.json()[2]["title"] == str(mock_post.title)


@pytest.mark.asyncio
async def test_get_single_post(default_client: httpx.AsyncClient) -> None:
    response = await default_client.get("/posts/1")
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
                           access_token: str) -> None:
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

    response = await default_client.put("/posts/1",
                                        json=payload,
                                        headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_delete_post(default_client: httpx.AsyncClient,
                           access_token: str) -> None:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {'message': 'Post sucessfully deleted'}

    response = await default_client.delete("/posts/2",
                                           headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response
