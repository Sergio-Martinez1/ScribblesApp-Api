from sqlalchemy.orm import Session
from sqlalchemy import desc
from models.models import Post as PostModel
from models.models import User as UserModel
from models.models import Tag as TagModel
from schemas.post import PostIn
from fastapi import HTTPException, status


class PostService():

    def __init__(self):
        pass

    async def get_posts(self, db: Session):
        posts = db.query(PostModel).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No posts found')
        return posts

    async def get_home_posts(self, username: str, db: Session, offset: int,
                             limit: int):
        user = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User does not exist')
        posts = db.query(PostModel).filter(
            PostModel.id.not_in(
                user.prohibited_posts if user.prohibited_posts else [])
        ).order_by(desc(PostModel.id)).offset(offset).limit(limit).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Not posts found')
        return posts

    async def get_my_posts(self, username: str, db: Session, offset: int,
                           limit: int):
        user = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='User does not exist')
        posts = db.query(PostModel).filter(
            PostModel.user_id == user.id).offset(offset).limit(limit).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Not posts found')
        return posts

    async def get_posts_with_tag(self, db: Session, tag_content: str,
                                 limit: int, offset: int):
        posts = db.query(PostModel).join(TagModel).filter(
            TagModel.content == tag_content).offset(offset).limit(limit).all()

        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No posts found with the specified tag")

        return posts

    async def get_posts_pagination(self, db: Session, limit: int, offset: int):
        posts = db.query(PostModel).order_by(desc(
            PostModel.id)).offset(offset).limit(limit).all()
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No posts found')
        return posts

    async def get_posts_by_user_id(self, db: Session, user_id: int):
        posts = db.query(PostModel).join(UserModel).filter(
            UserModel.id == user_id).all()

        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="No posts found for this user")

        return posts

    async def get_post(self, id: int, db: Session):
        post = db.query(PostModel).filter(PostModel.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Post not found')
        return post

    async def create_post(self, db: Session, post: PostIn, username: str):
        creator = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not creator:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Sign in first")

        new_post = PostModel(content=None, thumbnail=None, user_id=creator.id)

        if post.content is not None:
            new_post.content = post.content
        if post.thumbnail is not None:
            new_post.thumbnail = post.thumbnail

        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        if post.tags:
            post_created = db.query(PostModel).filter(
                PostModel.user_id == creator.id).order_by(desc(
                    PostModel.id)).first()
            for tag in post.tags:
                new_tag = TagModel(content=tag, post_id=post_created.id)
                db.add(new_tag)
            db.commit()
        return

    async def update_post(self, db: Session, new_post: PostIn, id: int,
                          username: str):
        post = db.query(PostModel).filter(PostModel.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Post not found")

        creator = db.query(UserModel).filter(
            UserModel.id == post.user_id).first()
        if username != creator.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Operation not allowed")

        if post.tags:
            for tag in post.tags:
                db.delete(tag)
        if new_post.tags:
            for tag in new_post.tags:
                new_tag = TagModel(content=tag, post_id=id)
                db.add(new_tag)

        post.content = None
        post.thumbnail = None

        if new_post.content is not None:
            post.content = new_post.content
        if new_post.thumbnail is not None:
            post.thumbnail = new_post.thumbnail

        db.add(post)
        db.commit()

        return

    async def delete_post(self, db: Session, id: int, username: str):
        post = db.query(PostModel).filter(PostModel.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Post not found")

        creator = db.query(UserModel).filter(
            UserModel.id == post.user_id).first()
        if username != creator.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Operation not allowed")

        db.delete(post)
        db.commit()
        return

    async def dont_show_post(self, db: Session, id: int, username: str):
        user = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        post = db.query(PostModel).filter(PostModel.id == id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Post does not exist")
        if user.prohibited_posts is not None and id in user.prohibited_posts:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Post already added")

        if user.prohibited_posts is None:
            user.prohibited_posts = []

        user.prohibited_posts += [id]

        db.add(user)
        db.commit()
        return
