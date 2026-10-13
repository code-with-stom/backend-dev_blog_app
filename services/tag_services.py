from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from utils.helpers import generate_slug
from models import User, Tag
from schemas.tag import TagData
from utils.enums import Roles

class TagService:
    @staticmethod
    def create_tag(db: Session, username: str, tag_data: TagData):
        user = db.query(User).filter(User.username == username).first()
        
        if user is None: 
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User doesn't exists!"
            )
            
        if user.is_active is not True:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is not active!"
            )
            
        tag = Tag(
            name=tag_data.name,
            slug=generate_slug(tag_data.name)
        )
        
        db.add(tag)
        db.commit()
        db.refresh(tag)
        
        return tag
    
    @staticmethod
    def delete_tag(db: Session, username: str, tag_slug: str):
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found!"
            )
            
        if user.role is not Roles.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You must be an admin to delete this."
            )
            
        tag = db.query(Tag).filter(Tag.slug == tag_slug).first()
        if tag is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found."
            )
            
        db.delete(tag)
        db.commit()
        
        return None