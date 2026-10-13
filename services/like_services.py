from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.likes import Like
from schemas.like import LikeCreate, LikeResponse
from models.users import User
from models.posts import Post

class LikeService:
    @staticmethod
    def like_post(db: Session, username: str, post_slug: str):
        # Check if user exists
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {username} does not exist!"
            )
        
        # Check if post exists
        post = db.query(Post).filter(Post.slug == post_slug).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post {post_slug} does not exist!"
            )
        
        # Check for an existing like
        existing_like = db.query(Like).filter(
            Like.user_id == user.id,
            Like.post_id == post.id
        ).first()

        if existing_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already liked this post."
            )
            
        like = Like(
            post_id=post.id,
            user_id=user.id
        )
        
        try:
            db.add(like)
            db.commit()
            db.refresh(like)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error adding like."
            )
            
        return LikeResponse.model_validate(like)
    
    @staticmethod
    def remove_like(db: Session, username: str, post_slug: str):
        # Check if user exists
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {username} does not exist!"
            )
        
        # Check if post exists
        post = db.query(Post).filter(Post.slug == post_slug).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post {post_slug} does not exist!"
            )
        
        # Check for an existing like
        existing_like = db.query(Like).filter(
            Like.user_id == user.id,
            Like.post_id == post.id
        ).first()

        if not existing_like:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have not liked this."
            )
            
        try:
            db.delete(existing_like)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error removing like."
            )
            
        return None