from fastapi import APIRouter

from app.api.endpoints import auth, recipes

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/api/auth", tags=["auth"])
api_router.include_router(recipes.router, prefix="/api/recipes", tags=["recipes"])