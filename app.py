from fastapi import FastAPI,APIRouter
from core.config import settings
from core.exception_handling import register_exception_handlers
from api.v1.endpoints.github import router as github_router

settings = settings

v1_router = APIRouter(prefix='/api/v1')
v1_router.include_router(github_router)

app = FastAPI(title=settings.app_name)
register_exception_handlers(app)
app.include_router(v1_router)

