from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CategorySchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    slug: str
    updated_at: datetime | None = None
    
class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    
class CategoryResponse(BaseModel):
    name: str
    description: str | None = None
    slug: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    slug: str | None = None
    updated_at: datetime