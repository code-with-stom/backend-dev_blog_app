from fastapi import APIRouter, Depends
from services.tag_services import TagService
from core.db_config import db_dependency
from core.dependency import get_current_user
from schemas.tag import TagData

router = APIRouter(
    prefix="/tag",
    tags=["tag"]
)

@router.post("/create")
def add_tag(db: db_dependency, data: TagData, username: str = Depends(get_current_user)):
    detail = TagService.create_tag(db, username, data)
    return {"detail": detail}