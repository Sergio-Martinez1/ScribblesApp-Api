from sqlalchemy import Column, Integer
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from db_config.database import Base


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='reactions')
