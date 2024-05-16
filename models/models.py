from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
from db_config.database import Base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())

    profile_photo = Column(String, nullable=True)
    cover_photo = Column(String, nullable=True)
    description = Column(String, nullable=True)
    personal_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    prohibited_posts = Column(MutableList.as_mutable(ARRAY(Integer)),
                              nullable=True)
    dark_mode = Column(String, nullable=True)
    color_scheme = Column(String, nullable = True)
    # A revision
    reactions = relationship('Reaction',
                             back_populates='user',
                             cascade='all, delete')
    comments = relationship('Comment',
                            back_populates='user',
                            order_by='Comment.id.desc()',
                            cascade='all, delete')
    posts = relationship('Post',
                         back_populates='user',
                         order_by='Post.id.desc()',
                         cascade='all, delete')


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    content = Column(String)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='tags')


class Reaction(Base):
    __tablename__ = "reactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship('Post', back_populates='reactions')
    user = relationship('User', back_populates='reactions')


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    thumbnail = Column(String, nullable=True)
    content = Column(String, nullable=True)
    publication_date = Column(DateTime(timezone=True),
                              server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')
    tags = relationship('Tag', back_populates='post', cascade='all, delete')
    reactions = relationship('Reaction',
                             back_populates='post',
                             cascade='all, delete')
    comments = relationship('Comment',
                            back_populates='post',
                            order_by='Comment.id.desc()',
                            cascade='all, delete')

    @property
    def num_comments(self):
        return len(self.comments)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    content = Column(String)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
