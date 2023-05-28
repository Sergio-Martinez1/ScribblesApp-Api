from sqlalchemy import Column, Integer, String, DateTime
from db_config.database import Base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    image = Column(String, nullable=True)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='tags')


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='reactions')


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    thumbnail = Column(String)
    content = Column(String)
    publication_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    tags = relationship('Tag', back_populates='post')
    reactions = relationship('Reaction', back_populates='post')
    comments = relationship('Comment', back_populates='post')


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    post = relationship('Post', back_populates='comments')
