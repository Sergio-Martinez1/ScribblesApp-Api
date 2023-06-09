import httpx
import pytest
from models.models import Post, Reaction, User
from db_config.database import SessionLocal
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
async def mock_post(mock_user: User) -> Reaction:
    new_post = Post(
        title="Test Post",
        thumbnail="https://fakeimage.com",
        content="This a test post",
        publication_date="2023-06-01",
        user_id=1
    )
    db = SessionLocal()
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    db.close()
    yield new_post


@pytest.fixture(scope="module")
async def mock_reaction(mock_post: Post) -> Reaction:
    db = SessionLocal()

    reaction_to_delete = Reaction(
        user_id=1,
        post_id=1
    )
    db.add(reaction_to_delete)
    db.commit()
    db.refresh(reaction_to_delete)
    db.close()

    new_reaction = Reaction(
        user_id=1,
        post_id=1
    )
    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    db.close()
    yield new_reaction


@pytest.mark.asyncio
async def test_get_reactions(default_client: httpx.AsyncClient,
                             mock_reaction: Reaction) -> None:
    response = await default_client.get("/reactions/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_reaction(default_client: httpx.AsyncClient,
                               access_token: str) -> None:
    payload = {
        "user_id": 1,
        "post_id": 1
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {"message": "Succesful reaction created."}

    response = await default_client.post("/reactions/",
                                         json=payload,
                                         headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_delete_reaction(default_client: httpx.AsyncClient,
                               access_token: str) -> None:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {"message": "Succesful reaction deleted."}

    response = await default_client.delete("/reactions/1",
                                           headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response
