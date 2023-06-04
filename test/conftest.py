import asyncio
import httpx
import pytest

from main import app
from models.models import User
from models.models import Post


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def default_client():
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client
# # Clean up resources
#     await Event.find_all().delete()
#     await User.find_all().delete()
