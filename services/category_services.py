from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.category import CategoryCreate, CategoryResponse
from models.users import User
from utils.enums import Roles
from utils.helpers import generate_slug
from models.categories import Category

class CategoryService:
    @staticmethod
    def create_category(db: Session, data: CategoryCreate, admin_username: str):
        # Check if the user is an admin
        admin = db.query(User).filter(User.username == admin_username).first()
        if admin.role != Roles.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin privileges required to create a category."
            )
        # Create a new category and add it to the database
        new_category = Category(
            name=data.name,
            description=data.description,
            slug=generate_slug(data.name),
            created_at=datetime.utcnow()
        )
        try:
            db.add(new_category)
            db.commit()
            db.refresh(new_category)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't add category to database: {e}"
            )
        return CategoryResponse.model_validate(new_category)

    @staticmethod
    def update_category(db: Session, category_id: int, data: CategoryCreate, admin_username: str):
        # Check if the user is an admin
        admin = db.query(User).filter(User.username == admin_username).first()
        if admin.role != Roles.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin privileges required to update a category."
            )
        # Get the category from the database
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        # Update the category
        if data.name is not None:
            category.name = data.name
            category.slug = generate_slug(data.name)
        if data.description is not None:
            category.description = data.description
        category.updated_at = datetime.utcnow()
        try:
            db.commit()
            db.refresh(category)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't update category in database: {e}"
            )
        return CategoryResponse.model_validate(category)
    
    @staticmethod
    def delete_category(db: Session, category_id: int, admin_username: str):
        # Check if the user is an admin
        admin = db.query(User).filter(User.username == admin_username).first()
        if admin.role != Roles.ADMIN.value:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Admin privileges required to delete a category."
            )
        # Get the category from the database
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        try:
            db.delete(category)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't delete category from database: {e}"
            )
        return None
    
    @staticmethod
    def get_all_categories(db: Session):
        categories = db.query(Category).all()
        return [CategoryResponse.model_validate(category) for category in categories]

    @staticmethod
    def get_category_by_slug(db: Session, category_slug: str):
        category = db.query(Category).filter(Category.slug == category_slug).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return CategoryResponse.model_validate(category)