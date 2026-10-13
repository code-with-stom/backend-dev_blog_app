from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from core.config import settings
from routes import *
from core.db_config import init_db
from core.config import settings
import models  # Import models to ensure they are registered with SQLAlchemy

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=f"{settings.PROJECT_VERSION}"
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.JWT_SECRET
)

# Start database Connection
init_db()

# Include all the routers
app.include_router(user_routes.user_router)
app.include_router(post_routes.router)
app.include_router(user_routes.admin_router)
app.include_router(category_routes.router)
app.include_router(auth_routes.router)
app.include_router(comment_routes.router)
app.include_router(tag_routes.router)
app.include_router(search_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Dev Blog App"}