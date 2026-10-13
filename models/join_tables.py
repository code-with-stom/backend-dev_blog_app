from sqlalchemy import Column, Integer, ForeignKey
from core.db_config import Base

class TagsPosts(Base):
    __tablename__ = "tags_posts"

    tags_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
    posts_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)