from fastapi import FastAPI
from routes.user import users_route
from routes.reaction import reactions_router
from routes.comment import comments_router
from routes.tag import tags_router
from routes.post import posts_router
from db_config.database import Base, engine

app = FastAPI()

app.title = "Scribbles API"
app.version = "0.0.1"
app.include_router(users_route)
app.include_router(reactions_router)
app.include_router(tags_router)
app.include_router(comments_router)
app.include_router(posts_router)

Base.metadata.create_all(bind=engine)
