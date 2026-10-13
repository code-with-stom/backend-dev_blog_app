from pydantic import BaseModel, ConfigDict

class TagSchema(BaseModel):
    id: int
    name: str
    slug: str

class TagData(BaseModel):
    name: str

class TagResponse(BaseModel):
    id: int
    name: str
    slug: str
    
    model_config = ConfigDict(from_attributes=True)