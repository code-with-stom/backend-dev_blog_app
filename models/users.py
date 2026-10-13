from sqlalchemy import Boolean, Column, String, Integer, Text
from sqlalchemy.orm import relationship
from core.db_config import Base
from utils.enums import Roles

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False)
    role = Column(String, default=Roles.USER.value)
    bio = Column(Text, nullable=True)
    google_id = Column(String, nullable=True, unique=True, index=True)
    
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")