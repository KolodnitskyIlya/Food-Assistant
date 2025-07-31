from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.schemas.recipe import RecipeCreate, RecipeResponse
from app.services.recipe import RecipeService
from app.core.security import get_current_user_id

router = APIRouter()


@router.post("/", response_model=RecipeResponse)
async def create_recipe(
    recipe: RecipeCreate,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await RecipeService.create_recipe(db, recipe, user_id)


@router.get("/", response_model=List[RecipeResponse])
async def get_user_recipes(
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    return await RecipeService.get_user_recipes(db, user_id)