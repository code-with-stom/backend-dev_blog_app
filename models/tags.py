from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.db_config import Base

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    posts = relationship("Post", secondary="tags_posts", back_populates="tags")