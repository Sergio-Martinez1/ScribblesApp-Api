from sqlalchemy import Column, Integer, String, Date, ARRAY
from db_config.database import Base
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    creation_date = Column(Date)

    profile_photo = Column(String, nullable=True)
    cover_photo = Column(String, nullable=True)
    description = Column(String, nullable=True)
    personal_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    prohibited_posts = Column(ARRAY(Integer), nullable=True)
    # A revision
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')


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


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    thumbnail = Column(String)
    content = Column(String)
    publication_date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')
    tags = relationship('Tag', back_populates='post')
    reactions = relationship('Reaction', back_populates='post')
    comments = relationship('Comment',
                            back_populates='post',
                            order_by='Comment.id.desc()')

    @property
    def num_comments(self):
        return len(self.comments)


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    content = Column(String)
    creation_date = Column(Date)
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
