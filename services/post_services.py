from fastapi import HTTPException, status, Query
from datetime import datetime
from sqlalchemy.orm import Session
from utils.helpers import generate_slug
from models.posts import Post
from models.tags import Tag
from schemas.post import PostCreate, PostResponse
from schemas.tag import TagData
from models.users import User
from models.categories import Category
from utils.enums import PostStatus
from services.tag_services import TagService

class PostService:
    @staticmethod
    def create_post(db: Session, data: PostCreate, username: str):
        # Check if the user is active
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not Found."
            )
        slug = generate_slug(data.title)
        
        tag_objects = []
        
        for tag_data in data.tags:
            tag_slug = generate_slug(tag_data.name)
            
            tag = db.query(Tag).filter(Tag.slug == tag_slug).first()
            
            if tag is None:
                tag = TagService.create_tag(db, username, TagData(name=tag_data.name))
                
            tag_objects.append(tag)
        
        new_post = Post(
            title=data.title, 
            content=data.content, 
            slug=slug, 
            category_id=data.category_id,
            created_at=datetime.utcnow(),
            status=data.status,
            author=user,
            tags=tag_objects
        )
        try:
            db.add(new_post)
            db.commit()
            db.refresh(new_post)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't add post to database: {e}"
            )
        return PostResponse.model_validate(new_post)
    
    @staticmethod
    def update_post(db: Session, post_slug: str, data: PostCreate, username: str):
        # Check if the user and post exists
        user = db.query(User).filter(User.username == username).first()
        post = db.query(Post).filter(Post.slug == post_slug).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not Found."
            )
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        if post.author_id is not user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This post belongs to someone else."
            )
        # Update fields if not empty.
        if data.title is not None:
            post.title = data.title
            post.slug = generate_slug(data.title)
        if data.content is not None:
            post.content = data.content
        if data.category_id is not None:
            post.category_id = data.category_id
        if data.status is not None:
            if data.status == "draft":
                post.status = PostStatus.DRAFT.value
            if data.status == "published":
                post.status = PostStatus.PUBLISHED.value
        # Update the update timestamp always.
        post.updated_at = datetime.utcnow()
        try:
            db.commit()
            db.refresh(post)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't update post in database: {e}"
            )
        return PostResponse.model_validate(post)
    
    @staticmethod
    def delete_post(db: Session, post_slug: str, username: str):
        # Check if the user exists
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not Found."
            )
        post = db.query(Post).filter(Post.slug == post_slug).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        try:
            db.delete(post)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't delete post from database: {e}"
            )
        return None
    
    @staticmethod
    def get_post(db: Session, slug: str):
        post = db.query(Post).filter(Post.slug == slug).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        return PostResponse.model_validate(post)
    
    @staticmethod
    def get_posts(db: Session, limit: int, page: int, category: str | None = None):
        # For pagination
        offset = (page - 1) * limit
        
        if category:
            cat = category.lower()
            db_cat = db.query(Category).filter(Category.slug == cat).first()        
            if db_cat is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Given category doesn't exist!"
                )
                
            posts = db.query(Post).filter_by(category_id=db_cat.id).offset(offset).limit(limit).all()
            post_list = [PostResponse.model_validate(post) for post in posts]
            
            return {
                "list": post_list,
                "count": len(post_list)
            }
            
        posts = db.query(Post).offset(offset).limit(limit).all()
        post_list = [PostResponse.model_validate(post) for post in posts]
        
        return {
            "list": post_list,
            "count": len(post_list)
        }