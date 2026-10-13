from fastapi import APIRouter
from core.db_config import db_dependency
from services.category_services import CategoryService

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/{category_slug}")
def get_category(
    db: db_dependency,
    category_slug: str
):
    category = CategoryService.get_category_by_slug(db, category_slug)
    if category:
        return {
            "detail": "Category Retrieved",
            "category": category
        }

@router.get("/")
def get_all_categories(
    db: db_dependency
):
    categories = CategoryService.get_all_categories(db)
    return {
        "detail": "Categories Retrieved",
        "categories": categories
    }