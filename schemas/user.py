from pydantic import BaseModel, EmailStr, ConfigDict
from utils.enums import Roles
from schemas.post import PostResponse

class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool
    role: str
    bio: str | None = None
    posts: list | None = []

class UserResponse(BaseModel):
    username: str
    email: EmailStr
    role: str | None = Roles.USER.value # default value is "user"
    bio: str | None = None
    posts: list[PostResponse] | None = []
    # comments: list[CommentResponse] | None = None
    
    model_config = ConfigDict(from_attributes=True)
    
class UserData(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool
    role: str | None = Roles.USER.value # default value is "user"
    
class UserUpdateData(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    bio: str | None = None

class UserAuth(BaseModel):
    username: str
    email: EmailStr
    password: str