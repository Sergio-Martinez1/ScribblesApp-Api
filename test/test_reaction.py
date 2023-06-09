import httpx
import pytest
from models.models import Post, Reaction, User
from db_config.database import SessionLocal
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


@pytest.fixture(scope="module")
async def mock_reaction(mock_post: Post, mock_user: User) -> Reaction:
    db = SessionLocal()

    reaction_to_delete = Reaction(user_id=mock_user.id, post_id=mock_post.id)
    db.add(reaction_to_delete)
    db.commit()
    db.refresh(reaction_to_delete)
    db.close()

    new_reaction = Reaction(user_id=mock_user.id, post_id=mock_post.id)
    db.add(new_reaction)
    db.commit()
    db.refresh(new_reaction)
    db.close()
    stored_reaction = db.query(Reaction).filter(
        Reaction.user_id == mock_user.id).first()
    yield stored_reaction


@pytest.mark.asyncio
async def test_get_reactions(default_client: httpx.AsyncClient,
                             mock_reaction: Reaction) -> None:
    response = await default_client.get("/reactions/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_reaction(default_client: httpx.AsyncClient,
                               access_token: str, mock_user: User,
                               mock_post: Post) -> None:
    payload = {"user_id": mock_user.id, "post_id": mock_post.id}
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
                               access_token: str,
                               mock_reaction: Reaction) -> None:
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    test_response = {"message": "Succesful reaction deleted."}

    response = await default_client.delete(f"/reactions/{mock_reaction.id}",
                                           headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response
