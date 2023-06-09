from fastapi import FastAPI
from routes.user import users_route
from routes.reaction import reactions_router
from routes.comment import comments_router
from routes.tag import tags_router
from routes.post import posts_router
from routes.upload import upload_router
from db_config.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.title = "Scribbles API"
app.version = "0.0.1"
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.include_router(users_route)
app.include_router(reactions_router)
app.include_router(tags_router)
app.include_router(comments_router)
app.include_router(posts_router)
app.include_router(upload_router)
app.mount('/files', StaticFiles(directory='files'), name='files')

Base.metadata.create_all(bind=engine)
