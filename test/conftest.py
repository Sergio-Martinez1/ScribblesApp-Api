import asyncio
import httpx
import pytest

from main import app
from models.models import User
from models.models import Post
from models.models import Tag
from models.models import Reaction
from models.models import Comment
from db_config.database import SessionLocal


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def default_client():
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client


# Clean up resources
    db = SessionLocal()
    db.query(Comment).delete()
    db.query(Reaction).delete()
    db.query(Tag).delete()
    db.query(Post).delete()
    db.query(User).delete()
    db.commit()
