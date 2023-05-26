from sqlalchemy import Column, Integer, String
from db_config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    image = Column(String, nullable=True)
