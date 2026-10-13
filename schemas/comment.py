from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CommentSchema(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class CommentData(BaseModel):
    content: str
    
class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int | None = None
    post_id: int
    created_at: datetime
    updated_at: datetime | None = None
    
    model_config = ConfigDict(from_attributes=True)