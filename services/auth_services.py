from fastapi import status, HTTPException, Request
from sqlalchemy.orm import Session
from schemas.user import UserAuth
from schemas.token import TokenData
from auth.auth_handler import create_access_token
from utils.helpers import hash_password, verify_password, generate_username
from models.users import User
from utils.enums import Roles
from auth.auth_bearer import oauth
from core.config import settings

class AuthService:
    @staticmethod
    def user_signup(db: Session, data: UserAuth):
        # Check if user exists
        user = db.query(User).filter(User.username == data.username).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User exists"
            )
        # Create a user and add it the database
        new_user = User(
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
            is_active=True,
            role=Roles.USER.value
        )
        try:
            db.add(new_user)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Couldn't add user to database: {e}"
            )
        return {"detail": "User Created"}
    
    @staticmethod
    def user_login(db: Session, username: str, password: str):
        # Get user from database
        user = db.query(User).filter(User.username == username).first()
        if verify_password(password, user.hashed_password):
            return user
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Username or Password"
        )
    
    @staticmethod
    async def github_login(request: Request):
        redirect_uri = settings.REDIRECT_URI

        return await oauth.github.authorize_redirect(
            request,
            redirect_uri
        )
        
    @staticmethod
    async def google_callback(request: Request, db: Session ):
        # Exchange Google authorization code for token
        token = await oauth.google.authorize_access_token(request)
        
        userinfo = token["userinfo"]

        google_id = userinfo["sub"]
        email = userinfo["email"]
        # name = userinfo["name"]

        user = db.query(User).filter(User.google_id == google_id).first()
        # Check if Google-linked account is present in the database, if not
        # also check if user with the email exists in our database
        if user is None:
            user = db.query(User).filter(User.email == email).first()
            if user is not None:
                user.google_id = google_id
                db.commit()
                db.refresh(user)
            
        if user is None:
            username = generate_username(email)
            
            user = User(
                google_id=google_id,
                username=username,
                email=email,
                hashed_password=None,
                role=Roles.USER.value,
                is_active=True,
            )            

            db.add(user)
            db.commit()
            db.refresh(user)

        # Create YOUR JWT
        access_token = create_access_token(
            TokenData(
                username=user.username,
                is_active=user.is_active,
                role=user.role
            )
        )

        # Return your application's token
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }