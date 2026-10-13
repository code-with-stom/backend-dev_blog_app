from fastapi import APIRouter, Depends, Query
from schemas.user import UserUpdateData
from core.db_config import db_dependency
from core.dependency import get_current_user
from services.user_services import AdminService, UserService
from schemas.category import CategoryCreate
from services.category_services import CategoryService
from services.tag_services import TagService

user_router = APIRouter(
    prefix="/users",
    tags=["user"]
)

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@admin_router.post("/create_category")
def create_category(
    db: db_dependency,
    data: CategoryCreate,
    username: str = Depends(get_current_user)
):
    category = CategoryService.create_category(db, data, username)
    if category:
        return {
            "detail": "Category Created",
            "category": category
        }
        
@admin_router.put("/{category_id}")
def update_category(
    db: db_dependency,
    category_id: int,
    data: CategoryCreate,
    username: str = Depends(get_current_user)
):
    category = CategoryService.update_category(db, category_id, data, username)
    if category:
        return {
            "detail": "Category Updated",
            "category": category
        }

@admin_router.delete("/{category_id}")
def delete_category(
    db: db_dependency,
    category_id: int,
    username: str = Depends(get_current_user)
):
    category = CategoryService.delete_category(db, category_id, username)
    if category is None:
        return {
            "detail": "Category Deleted",
            "category": category
        }

@admin_router.get("/")
def admin_dashboard(
    db: db_dependency, 
    username: str = Depends(get_current_user)
):
    detail = AdminService.dashboard(db, username)
    return detail

@admin_router.get("/user/{id}")
def get_user(
    db: db_dependency, 
    id: int,
    admin_username: str = Depends(get_current_user)
):
    return AdminService.get_user_by_id(db, admin_username, id)

@admin_router.get("/users")
def get_all_users(
    db: db_dependency,
    username: str = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1)
):
    return AdminService.users_list(db, username)

@admin_router.get("/posts")
def get_all_posts(
    db: db_dependency,
    username: str = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    category: str | None = Query(None)    
):
    return AdminService.posts_list(db, username, limit, page, category)

@admin_router.delete("/tag/delete")
def delete_tag(db: db_dependency, tag_slug: str, username: str = Depends(get_current_user)):
    detail = TagService.delete_tag(db, username, tag_slug)
    return {"detail": f"Tag {tag_slug} deleted." if detail is None else "An Error Occured"}

@user_router.get("/profile")
def profile(db: db_dependency, username: str = Depends(get_current_user)):
    return UserService.get_user(db, username)

@user_router.put("/update_profile")
def update_profile(
    db: db_dependency,
    update_data: UserUpdateData,
    username: str = Depends(get_current_user)
):
    return UserService.update_user(db, username, update_data)

@user_router.delete("/delete_profile")
def delete_profile(
    db: db_dependency,
    username: str = Depends(get_current_user)
):
    detail = UserService.delete_user(db, username)
    return {"detail": detail}

@user_router.get("/{username}")
def user(db: db_dependency, username: str):
    return UserService.get_user_by_username(db, username)