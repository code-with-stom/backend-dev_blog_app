from fastapi import APIRouter, Depends, Query
from core.dependency import get_current_user
from schemas.post import PostCreate
from core.db_config import db_dependency
from services.post_services import PostService
from services.like_services import LikeService

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/create_post")
def create_post(
    data: PostCreate, 
    db: db_dependency, 
    username: str = Depends(get_current_user)
):
    post = PostService.create_post(db, data, username)
    if post:
        return {
            "detail": "Post Created", 
            "post": post
        }
        
@router.put("/{post_slug}")
def update_post(
    post_slug: str, 
    data: PostCreate, 
    db: db_dependency, 
    username: str = Depends(get_current_user)
):
    post = PostService.update_post(db, post_slug, data, username)
    if post:
        return {
            "detail": "Post Updated", 
            "post": post
        }
        
@router.delete("/{post_slug}")
def delete_post(
    db: db_dependency,
    post_slug: str,
    username: str = Depends(get_current_user)
):
    post = PostService.delete_post(db, post_slug, username)
    if post is None:
        return {
            "detail": "Post Deleted", 
            "post": post
        }
        
@router.get("/{post_slug}")
def get_post(
    db: db_dependency,
    post_slug: str
):
    post = PostService.get_post(db, post_slug)
    if post:
        return {
            "detail": "Post Found", 
            "post": post
        }
        
@router.get("/")
def get_posts(
    db: db_dependency, 
    limit: int = Query(10, ge=1, le=50), 
    page: int = Query(ge=1),
    category: str | None = Query(None),
):  
    posts = PostService.get_posts(db, limit, page, category)
    return {
        "page": page,
        "limit": limit,
        "number_of_posts": posts["count"],
        "posts": posts["list"]
    }
    
@router.post("/{post_slug}/like")
def like_a_post(
    db: db_dependency,
    post_slug: str,
    username: str = Depends(get_current_user)
):
    data = LikeService.like_post(db, username, post_slug)
    
    return {
        "detail": f"Post {post_slug} liked.",
        "data": data
    }