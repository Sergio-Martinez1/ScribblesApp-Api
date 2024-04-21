import asyncio
import httpx
import pytest

from main import app
from models.models import User
from models.models import Post
from models.models import Tag
from models.models import Reaction
from models.models import Comment
import pytest_asyncio
from db_config.database import SessionLocal


@pytest_asyncio.fixture(scope="session")
async def default_client():
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client
    db = SessionLocal()
    db.query(Comment).delete()
    db.query(Reaction).delete()
    db.query(Tag).delete()
    db.query(Post).delete()
    db.query(User).delete()
    db.commit()
