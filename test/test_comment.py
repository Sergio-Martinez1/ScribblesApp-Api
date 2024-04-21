import httpx
import pytest
import pytest_asyncio
from datetime import date
from auth.jwt_handler import create_access_token
from auth.hash_password import HashPassword
from db_config.database import SessionLocal
from models.models import User
from models.models import Post
from models.models import Comment

db = SessionLocal()


@pytest_asyncio.fixture(scope="module")
async def mock_user() -> User:
    test_password = "123456"
    hashed_password = HashPassword().create_hash(test_password)
    userModel = User(
        username="sergio",
        email="sergio@mail.com",
        password=hashed_password,
        profile_photo="http://image.com",
    )
    db.add(userModel)
    db.commit()
    db.refresh(userModel)
    stored_user = db.query(User).filter(
        User.username == userModel.username).first()
    yield stored_user


@pytest_asyncio.fixture(scope="module")
async def mock_access_token(mock_user: User) -> str:
    return create_access_token(mock_user.username)


@pytest_asyncio.fixture(scope="module")
async def mock_post(mock_user: User) -> Post:
    new_post = Post(thumbnail="http://image.com",
                    content="Some content for a test post",
                    user_id=mock_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    stored_post = db.query(Post).filter(Post.user_id == mock_user.id).first()
    yield stored_post


@pytest_asyncio.fixture(scope="module")
async def mock_comment(mock_user: User, mock_post: Post) -> Comment:
    new_comment = Comment(post_id=mock_post.id,
                          user_id=mock_user.id,
                          content="Some content for a test post")
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    stored_comment = db.query(Comment).filter(
        Comment.user_id == mock_user.id).first()
    yield stored_comment


@pytest.mark.asyncio
async def test_create_comment(default_client: httpx.AsyncClient,
                              mock_access_token: str, mock_post: Post):
    payload = {
        "content": "Some content for a comment",
        "post_id": mock_post.id
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mock_access_token}"
    }
    test_response = {"message": "Comment created successfully."}
    response = await default_client.post("/comments/",
                                         json=payload,
                                         headers=headers)
    assert response.status_code == 201
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_update_comment(default_client: httpx.AsyncClient,
                              mock_access_token: str, mock_comment: Comment):
    payload = {"content": "Some content for a comment"}
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mock_access_token}"
    }
    test_response = {"message": "Succesful comment update."}

    response = await default_client.put(f"/comments/{mock_comment.id}",
                                        json=payload,
                                        headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_delete_comment(default_client: httpx.AsyncClient,
                              mock_access_token: str, mock_comment: Comment):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {mock_access_token}"
    }
    test_response = {"message": "Succesful comment deleted."}
    response = await default_client.delete(f"/comments/{mock_comment.id}",
                                           headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response
