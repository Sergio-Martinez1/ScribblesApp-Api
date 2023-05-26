from fastapi import FastAPI
from routes.user import users_route
from db_config.database import Base, engine

app = FastAPI()

app.title = "Scribbles API"
app.version = "0.0.1"
app.include_router(users_route)

Base.metadata.create_all(bind=engine)
