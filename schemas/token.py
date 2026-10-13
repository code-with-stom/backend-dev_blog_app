from pydantic import BaseModel

class TokenData(BaseModel):
    username: str | None = None
    is_active: bool | None = None
    role: str | None = None