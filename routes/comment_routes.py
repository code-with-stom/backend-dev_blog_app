from fastapi import APIRouter, Depends
from services.comment_services import CommentService
from core.db_config import db_dependency
from core.dependency import get_current_user
from schemas.comment import CommentData

router = APIRouter(
    prefix="/comment",
    tags=["comment"]
)

@router.post("/{post_slug}")
def add_comment(
    db: db_dependency, 
    data: CommentData, 
    post_slug: str,  
    username: str = Depends(get_current_user)
):
    detail = CommentService.add_comment(db, username, data, post_slug)
    return {"detail": detail}

@router.patch("/{post_slug}")
def update_comment(
    db: db_dependency,
    data: CommentData,
    post_slug: str,
    comment_id: str,
    username: str = Depends(get_current_user)
):
    detail = CommentService.update_comment(db, username, data, post_slug, comment_id)  
    return {
        "message": "Comment Updated.",
        "detail": detail
    }  
    
@router.delete("/{post_slug}")
def delete_comment(
    db: db_dependency,
    post_slug: str,
    comment_id: int,
    username: str = Depends(get_current_user)
):
    detail = CommentService.delete_comment(db, post_slug, comment_id, username)
    return {"detail": "Comment removed." if detail is None else "Error in removing comment"}