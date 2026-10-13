from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from services import *
from models import *
from utils.enums import Roles
from schemas import *

class SearchService:
    @staticmethod
    def search_all(db: Session, search_str: str, username: str):
        try:
            users = db.query(User).filter(User.username.ilike(f"%{search_str.strip()}%"))
            posts = db.query(Post).filter(Post.title.ilike(f"%{search_str.strip()}%"))
            tags = db.query(Tag).filter(Tag.name.ilike(f"%{search_str.strip()}%"))
            categories = db.query(Category).filter(Category.name.ilike(f"%{search_str.strip()}%"))
            comments = db.query(Comment).filter(Comment.content.ilike(f"%{search_str.strip()}%"))
                    
            db_user = db.query(User).filter(User.username == username).first()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error while fetching from Database: {e}"
            )
            
        # If logged-in user isn't an admin
        if db_user.role != Roles.ADMIN.value:
            return {
                "users": [UserResponse.model_validate(user) for user in users.all()],
                "posts": [PostResponse.model_validate(post) for post in posts.all()],
                "categories": [CategoryResponse.model_validate(category) for category in categories.all()],
                "tags": [TagResponse.model_validate(tag) for tag in tags.all()]
            }
        else:   
            # If logged-in user is an admin
            return {
                "users": {
                    "count": users.count(),
                    "all": [UserResponse.model_validate(user) for user in users.all()]
                },
                "posts": {
                    "count": posts.count(),
                    "all": [PostResponse.model_validate(post) for post in posts.all()]
                },
                "categories": {
                    "count": categories.count(),
                    "all": [CategoryResponse.model_validate(category) for category in categories.all()]
                },
                "tags": {
                    "count": tags.count(),
                    "all": [TagResponse.model_validate(tag) for tag in tags.all()]
                },
                "comments": {
                    "count": comments.count(),
                    "all": [CommentResponse.model_validate(comment) for comment in comments.all()]
                }
            }