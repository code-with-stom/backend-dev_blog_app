from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from models.users import User
from schemas.user import UserResponse, UserUpdateData
from schemas.post import PostResponse
from utils.enums import Roles
from utils.helpers import hash_password
from models import *

class AdminService:
    @staticmethod
    def dashboard(db: Session, username: str):
        admin = db.query(User).filter(User.username == username).first()
        if admin is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User does not exists!"
            )
            
        if admin.role != Roles.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins Only."
            )
        try:
            total_users = db.query(User).count()
            total_tags = db.query(Tag).count()
            total_posts = db.query(Post).count()
            total_categories = db.query(Category).count()
            total_comments = db.query(Comment).count()
            return {
                "detail" : 
                    {
                        "total_users": total_users,
                        "total_tags": total_tags,
                        "total_posts": total_posts,
                        "total_categories": total_categories,
                        "total_comments": total_comments
                    }
                }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An error occured: {e}"
            )
        
    @staticmethod
    def users_list(db: Session, username: str, lim: int, page: int):
        try:
            admin = db.query(User).filter(User.username == username).first()
            if admin.role != Roles.ADMIN.value:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Admins Only."
                )
            
            # Pagination offset
            offset = (page - 1) * lim
            
            users = db.query(User).offset(offset).limit(lim).all()
            
            return {
                "detail": [UserResponse.model_validate(user) for user in users],
                "page": page,
                "admin": admin
            }
            
        except Exception as err:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't return users: {err}"
            )
            
    @staticmethod
    def posts_list(db: Session, username: str, lim: int, page: int, category: str | None = None):
        try:
            admin = db.query(User).filter(User.username == username).first()
            if admin.role != Roles.ADMIN.value:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Admins Only."
                )
            
            offset = (page - 1) * lim
                    
            if category:
                cat = category.lower()
                db_cat = db.query(Category).filter(Category.slug == cat).first()        
                if db_cat is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Given category doesn't exist!"
                    )
                    
                posts = db.query(Post).filter_by(category_id=db_cat.id).offset(offset).limit(lim).all()
                post_list = [PostResponse.model_validate(post) for post in posts]
                
                return {
                    "list": post_list,
                    "count": len(post_list)
                }
                
            posts = db.query(Post).offset(offset).limit(lim).all()
            post_list = [PostResponse.model_validate(post) for post in posts]
            
            return {
                "list": post_list,
                "count": len(post_list),
                "admin": admin
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't return posts: {e}"
            )
    
    @staticmethod            
    def get_user_by_id(db: Session, admin_username: str, id: int):
        # Return Admin
        admin = db.query(User).filter(User.username == admin_username).first()
        # Check if role is "admin"
        if admin.role != Roles.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admins Only."
            )
        user = db.query(User).filter(User.id == id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User doesn't exist! Create user."
            )
        return {
            "detail": UserResponse.model_validate(user),
            "admin": admin
        }
    
class UserService:    
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {username} doesn't exist! Create user."
            )
        user_res = UserResponse.model_validate(user)
        return {
            "detail": user_res
        }
        
    @staticmethod    
    def get_user(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {username} doesn't exist! Create user."
            )
        user_res = UserResponse.model_validate(user)
        return {
            "detail": user
        }
        
    @staticmethod
    def update_user(db: Session, username: str, update_data: UserUpdateData):
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {username} doesn't exist! Create user."
            )
        # Update username if provided
        if update_data.username is not None:
            user.username = update_data.username
        # Update email if provided
        if update_data.email is not None:
            user.email = update_data.email
        # Update password if provided
        if update_data.password is not None:
            user.hashed_password = hash_password(update_data.password)
        # Update bio if provided
        if update_data.bio is not None:
            user.bio = update_data.bio
        
        db.commit()
        db.refresh(user)
        return {
            "detail": f"User {username} updated successfully.",
            "user": UserResponse(
                username=user.username,
                email=user.email,
                role=user.role,
                bio=user.bio
            )
        }
    
    @staticmethod
    def delete_user(db: Session, username: str):
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exists!"
            )
        db.delete(user)
        db.commit()
        return f"Goodbye, {username}!"