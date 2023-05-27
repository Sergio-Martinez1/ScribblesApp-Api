from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.schema import ForeignKey
from db_config.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    thumbnail = Column(String)
    content = Column(String)
    publication_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
