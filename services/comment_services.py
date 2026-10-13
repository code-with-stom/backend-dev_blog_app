from fastapi import HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session
from models.comments import Comment
from schemas.comment import CommentData, CommentResponse
from models.users import User
from models.posts import Post
from  utils.enums import Roles


class CommentService:
    @staticmethod
    def add_comment(db: Session, username: str, data: CommentData, post_slug: str):
        # Check if user exists
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
            
        # Check if post exists 
        post = db.query(Post).filter(Post.slug == post_slug).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        comment = Comment(
            content=data.content,
            post_id=post.id,
            user_id=user.id,
            created_at=datetime.utcnow()
        )
        try:
            db.add(comment)
            db.commit()
            db.refresh(comment)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database Error."
            )
        
        return CommentResponse.model_validate(comment)
        
    @staticmethod
    def update_comment(
        db: Session, 
        username: str, 
        data: CommentData, 
        post_slug: str,
        comment_id: int
    ):
        # Check if user exists
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        # Check if post exists
        post = db.query(Post).filter(Post.slug == post_slug).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )
        
        # Check if comment exists
        comment = db.query(Comment).filter(Comment.id == comment_id, Comment.post_id == post.id).first()
        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment no longer exists or has been deleted."
            )
            
        # Check if user is authorized to update the comment
        if user.id != comment.user_id and user.role != Roles.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permission to update comment."
            )
            
        comment.content = data.content
        comment.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(comment)
        return CommentResponse.model_validate(comment)
    
    @staticmethod
    def delete_comment(db: Session, post_slug: str, id: int, username: str):
        # Check if user exists
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found."
            )
        
        # Check if post exists
        post = db.query(Post).filter(Post.slug == post_slug).first()
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Post not found"
            )
        
        # Check if comment exists    
        comment = db.query(Comment).filter(Comment.id == id, Comment.post_id == post.id).first()
        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment no longer exists or has been deleted."
            )
            
        # Check if user is authorized to update the comment
        if user.id != comment.user_id and user.role != Roles.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permission to delete comment."
            )
                    
        db.delete(comment)
        db.commit()
        
        return None