from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserAuth
from auth.auth_handler import create_access_token
from core.db_config import db_dependency
from services.auth_services import AuthService
from schemas.token import TokenData
from auth.auth_bearer import oauth
from core.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register")
def register_user(db: db_dependency, data: UserAuth):
    # Create a User and return the message
    message = AuthService.user_signup(db, data)
    return message

@router.post("/login")
def login(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = AuthService.user_login(db, form_data.username, form_data.password)
        return {
            "access_token": create_access_token(
                TokenData(
                    username=user.username,
                    is_active=user.is_active,
                    role=user.role
                )
            ),
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Couldn't login user: {e}"
        )
        
@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        settings.REDIRECT_URI,
    )

@router.get("/google/callback")
async def google_callback(request: Request, db: db_dependency):
    detail = await AuthService.google_callback(request, db)
    
    return {
        "message": "Google authentication successful",
        "detail": detail,
    }