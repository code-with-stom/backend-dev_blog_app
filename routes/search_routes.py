from fastapi import APIRouter, Depends, status, Query
from core.dependency import get_current_user
from core.db_config import db_dependency
from services.search_services import SearchService

router = APIRouter(
    prefix="/search",
    tags=["search"]
)

@router.get("/")
def search(db: db_dependency, username: str = Depends(get_current_user), search_str: str = Query(...)):
    return SearchService.search_all(db, search_str, username)