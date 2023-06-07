import httpx
import pytest
from models.models import Post
from db_config.database import SessionLocal
from auth.jwt_handler import create_access_token


@pytest.fixture(scope="module")
async def access_token() -> str:
    return create_access_token("pepe10121")


@pytest.fixture(scope="module")
async def mock_event() -> Post:
    new_post = Post(
        title="Test Post",
        thumbnail="https://fakeimage.com",
        content="This a test post",
        publication_date="2023-06-01",
        user_id=2
    )
    db = SessionLocal()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    yield new_post


@pytest.mark.asyncio
async def test_get_posts(default_client: httpx.AsyncClient,
                         mock_event: Post) -> None:
    response = await default_client.get("/posts/")
    assert response.status_code == 200
    assert response.json()[0]["title"] == str(mock_event.title)


@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient,
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
