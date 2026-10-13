from pydantic import ConfigDict, BaseModel
from datetime import datetime

class LikeCreate(BaseModel):
    is_liked: bool = True

class LikeResponse(BaseModel):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)