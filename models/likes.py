from sqlalchemy import Column, Integer, UniqueConstraint, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db_config import Base

class Like(Base):
    __tablename__ = "likes"
    
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "post_id",
            name="uq_for_like_user_post",
        ),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")