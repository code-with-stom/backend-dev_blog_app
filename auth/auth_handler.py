from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from core.config import settings
from schemas.token import TokenData

def create_access_token(data: TokenData):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_TIMEDELTA)
    to_encode = {
        "sub": data.username,
        "iat": datetime.utcnow(),
        "exp": expire,
        "is_active": data.is_active,
        "role": data.role
    }
    token = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        settings.JWT_ALGORITHM
    )
    return token

def decode_jwt(token: str):
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )