from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

oauth.register(
    name="google",
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    server_metadata_url=(
        "https://accounts.google.com/"
        ".well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid email profile"
    },
)
